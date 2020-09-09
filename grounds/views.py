from django.shortcuts import render
from django.http import HttpResponseNotFound

from .models import Ground, DISTRICTS, TYPES
from sport_grounds.secret_key import apikey


def grounds(request):
    if request.method == 'POST' and \
       (request.POST.get('dis') != 'all' or request.POST.get('tps') != 'all'):
        dis = request.POST.get('dis')
        tps = request.POST.get('tps')
        if dis == 'all':
            grds = Ground.objects.filter(type=tps)
        elif tps == 'all':
            grds = Ground.objects.filter(district=dis)
        else:
            grds = Ground.objects.filter(type=tps, district=dis)
        return render(request, 'grounds/grounds.html', {'grounds': grds,
                                                        'districts': DISTRICTS,
                                                        'types': TYPES})
    else:
        return render(request, 'grounds/grounds.html', {'grounds': Ground.objects.all(),
                                                        'districts': DISTRICTS,
                                                        'types': TYPES})


def ground(request, ground_id):
    try:
        grd = Ground.objects.get(id=ground_id)
        coordinates = [grd.get_x(), grd.get_y()]
        close_grounds = grd.close_grounds()
        return render(request, 'grounds/ground.html', {'ground': grd,
                                                       'images': grd.image_set.all(),
                                                       'coordinates': coordinates,
                                                       'close_grounds': close_grounds,
                                                       'key': apikey})
    except Ground.DoesNotExist:
        return HttpResponseNotFound('<h2>Нет такой площадки</h2>')


def add(request):
    if request.method == 'POST':
        grd = Ground()
        grd.add(request=request)
        return render(request, 'grounds/add.html', {'added': True})
    else:
        return render(request, 'grounds/add.html', {
            'added': False,
            'districts': DISTRICTS,
            'types': TYPES,
            'key': apikey
        })


def edit(request, ground_id):
    if request.method == 'POST':
        return render(request, 'grounds/edited.html')
    else:
        try:
            grd = Ground.objects.get(id=ground_id)
            if request.method == 'POST':
                grd.add(request=request)
                return render(request, 'grounds/edit.html', {'edited': True})
            else:
                return render(request, 'grounds/edit.html', {
                    'districts': DISTRICTS,
                    'types': TYPES,
                    'ground': grd
                })
        except Ground.DoesNotExist:
            return HttpResponseNotFound('<h2>Нет такой площадки</h2>')
