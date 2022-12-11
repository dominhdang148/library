from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Topic, Comment, Document
from .forms import DocumentForm


def home(request):
    documents = Document.objects.all()
    context = {'documents': documents}
    return render(request, 'base/home.html', context)


def document(request, pk):
    doc = Document.objects.get(id=pk)
    context = {'document': doc}
    return render(request, 'base/document.html', context)


def createDocument(request):
    form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/document_form.html', context)
