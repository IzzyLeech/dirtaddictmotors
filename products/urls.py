from django.urls import path, register_converter
from . import views
from .converters import FloatDecimalConverter

register_converter(FloatDecimalConverter, 'float_decimal')

urlpatterns = [
    path('', views.products_display, name='products'),
    path('manufacturer/<str:manufacturer_name>/', views.products_display, name='products_by_manufacturer'),
    path('engine/<float_decimal:engine_num>/', views.products_display, name='products_by_engine'),
    path('stroke/<float_decimal:stroke_num>/', views.products_display, name='products_by_stroke'),
]
