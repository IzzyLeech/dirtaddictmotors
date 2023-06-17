from django.shortcuts import render
from .models import Bikes


def products_display(request, manufacturer_name=None, engine_num=None, stroke_num=None):
    """View to display products based on optional filters"""

    bikes = Bikes.objects.all()

    selected_filters = []

    if manufacturer_name:
        bikes = bikes.filter(manufacturer=manufacturer_name)
        selected_filters.append(f'Manufacturer: {manufacturer_name}')

    if engine_num:
        bikes = bikes.filter(engine_capacity=engine_num)
        selected_filters.append(f'Engine Capacity: {engine_num}CC')

    if stroke_num:
        bikes = bikes.filter(stroke=stroke_num)
        selected_filters.append(f'Stroke: {stroke_num}')
        print(stroke_num)
        print(selected_filters)

    if not selected_filters:
        selected_filters.append('All Bikes')

    context = {
        'bikes': bikes,
        'selected_filters': selected_filters,
    }

    return render(request, 'products/products.html', context)
