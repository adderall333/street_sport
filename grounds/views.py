from django.shortcuts import render


def grounds(request):
    return render(request, 'grounds/grounds.html')


def add(request):
    return render(request, 'grounds/add.html')
