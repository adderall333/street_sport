from django.shortcuts import render
from grounds.models import Ground
from sport_grounds.secret_key import apikey


def map(request):
    grounds = Ground.objects.all()
    coordinates = [[ground.get_x(), ground.get_y()] for ground in grounds]
    return render(request, 'map/map.html', {'coordinates': coordinates, 'key': apikey})
