from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_display, name='products'),
    path('manufacturer/<str:manufacturer_name>/', views.products_by_manufacturer, name='products_by_manufacturer'),
]
