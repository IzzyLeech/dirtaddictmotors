from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('faq/', views.faq_view, name='faq'),
    path('delivery/', views.delivery_info, name='delivery'),
    path('get-random-bikes/', views.get_random_bikes, name='get_random_bikes')
]
