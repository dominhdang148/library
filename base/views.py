from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Topic, Comment, Document
from .forms import DocumentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib import messages
from .functions import handle_uploaded_file
import os


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not existed")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Wrong password or username")
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
    else:
        messages.error(request, "An Error occur during registration")
    context = {"form": form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    documents = Document.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(author__username__icontains=q) |
        Q(description__icontains=q))
    topics = Topic.objects.all()
    comments = Comment.objects.filter(
        Q(document__author__username=request.user.username) |
        Q(user__username=request.user.username)) if q == '' else Comment.objects.filter(
            Q(document__topic__name__icontains=q)
    )
    context = {'documents': documents, 'topics': topics, 'comments': comments}
    return render(request, 'base/home.html', context)


def document(request, pk):
    doc = Document.objects.get(id=pk)
    comments = doc.comment_set.all().order_by('-created')

    if request.method == 'POST':
        comment = Comment.objects.create(
            document=doc,
            user=request.user,
            body=request.POST.get('body')
        )
        return redirect('document', pk=doc.id)
    context = {'document': doc, 'comments': comments}
    return render(request, 'base/document.html', context)


def userProfile(request, pk):
    topics = Topic.objects.all()
    user = User.objects.get(id=pk)
    documents = user.document_set.all()
    context = {'user': user, 'documents': documents, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createDocument(request):
    form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            handle_uploaded_file(request.FILES['content'])
            document.author = request.user
            document.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/document_form.html', context)


@login_required(login_url='login')
def updateDocument(request, pk):
    document = Document.objects.get(id=pk)
    olddoc = document.content
    form = DocumentForm(instance=document)

    if request.user != document.author:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        print(olddoc)
        if form.is_valid():
           
            handle_uploaded_file(request.FILES['content'])
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/document_form.html', context)


@login_required(login_url='login')
def deleteDocument(request, pk):
    document = Document.objects.get(id=pk)
    print(document.content)
    if request.user != document.author:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        os.remove(f'base/static/upload/{document.content}')
        document.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': document})




@login_required(login_url='login')
def deleteComment(request, pk):
    document = request
    comment = Comment.objects.get(id=pk)
    if request.user != comment.user:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        comment.delete()
        return redirect('document')
    return render(request, 'base/delete.html', {'obj': comment})
