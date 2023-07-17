from django.urls import path, register_converter
from . import views
from .converters import FloatDecimalConverter

register_converter(FloatDecimalConverter, 'float_decimal')

urlpatterns = [
    path('', views.products_view, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path(
        'manufacturer/<str:manufacturer_name>/',
        views.products_view,
        name='products_by_manufacturer'),
    path(
        'engine/<float_decimal:engine_num>/',
        views.products_view,
        name='products_by_engine'),
    path(
        'stroke/<float_decimal:stroke_num>/',
        views.products_view,
        name='products_by_stroke'),
    path('add_bike/', views.add_bike, name='add_bike'),
    path('edit_bike/<int:product_id>/', views.edit_bike, name='edit_bike'),
    path(
        'delete_bike/<int:product_id>/',
        views.delete_bike,
        name='delete_bike'),
]
