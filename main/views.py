from django.shortcuts import render
from grounds.models import Ground, TYPES


def index(request):
    types = []
    for type in TYPES:
        types.append((type[0], type[1], len(Ground.objects.filter(type=type[0]))))
    return render(request, 'main/index.html', {'types': types})


def map(request):
    return render(request, 'map/map.html')
