from django.shortcuts import render
from django.http import HttpResponse

documents = [
    {'id': 1, 'name': 'Doraemon'},
    {'id': 2, 'name': 'Python Cookbook'},
    {'id': 3, 'name': 'Sherlock Holmes'},
    {'id': 4, 'name': 'Sudoku quiz'},
]


def home(request):

    context = {'documents': documents}
    return render(request, 'base/home.html', context)


def document(request, pk):
    doc = None
    for i in documents:
        if i['id'] == int(pk):
            doc = i
    context = {'document': doc}
    return render(request, 'base/document.html', context)
