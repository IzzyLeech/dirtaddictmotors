from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
    path('', views.products_display, name='products'),
    path('manufacturer/<str:manufacturer_name>/', views.products_by_manufacturer, name='products_by_manufacturer'),
    re_path(r'^engine/(?P<engine_num>\d+(\.\d+)?)/$', views.products_by_engine, name='products_by_engine'),
    re_path(r'^stroke/(?P<stroke_num>\d+(\.\d+)?)/$', views.products_by_stroke, name='products_by_stroke'),
]
