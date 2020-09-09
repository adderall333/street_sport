from django.shortcuts import render
from grounds.models import Ground
from sport_grounds.secret_key import apikey


def on_map(request):
    grounds = Ground.objects.all()
    data = [{"coords": [ground.get_x(), ground.get_y()],
             "desc": ground.short_description,
             "img": ground.main_image,
             "id": ground.id} for ground in grounds]
    return render(request, 'map/on_map.html', {'key': apikey, 'data': data})
