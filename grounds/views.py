from django.shortcuts import render
from django.http import HttpResponseNotFound

from .models import Ground
from sport_grounds.secret_key import apikey


def grounds(request):
    return render(request, 'grounds/grounds.html', {'grounds': Ground.objects.all()})


def ground(request, ground_id):
    try:
        return render(request, 'grounds/ground.html', {'ground': Ground.objects.get(id=ground_id)})
    except Ground.DoesNotExist:
        return HttpResponseNotFound('<h2>Нет такой площадки</h2>')


def add(request):
    if request.method == 'POST':
        ground = Ground()
        ground.add_or_edit(request=request)
        return render(request, 'grounds/add.html', {'added': True})
    else:
        return render(request, 'grounds/add.html', {
            'added': False,
            'districts': Ground.DISTRICTS,
            'types': Ground.TYPES,
            'key': apikey
        })


def edit(request, ground_id):
    try:
        ground = Ground.objects.get(id=ground_id)
        if request.method == 'POST':
            ground.add_or_edit(request=request)
            return render(request, 'grounds/edit.html', {'edited': True})
        else:
            return render(request, 'grounds/edit.html', {
                'edited': False,
                'districts': Ground.DISTRICTS,
                'types': Ground.TYPES,
                'ground': ground
            })
    except Ground.DoesNotExist:
        return HttpResponseNotFound('<h2>Нет такой площадки</h2>')