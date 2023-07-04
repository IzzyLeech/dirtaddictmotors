from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('get-random-bikes/', views.get_random_bikes, name='get_random_bikes')
]
