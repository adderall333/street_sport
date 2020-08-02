from django.urls import path
from . import views


urlpatterns = [
    path('', views.grounds),
    path('add/', views.add),
    path('<int:ground_id>/', views.ground),
    path('<int:ground_id>/edit/', views.edit)
]
