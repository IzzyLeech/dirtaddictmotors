from django.shortcuts import render, get_object_or_404
from django.db.models import Q
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
        engine_num = str(engine_num).split(".")[0]
        selected_filters.append(f'Engine Capacity: {engine_num} CC')

    if stroke_num:
        bikes = bikes.filter(stroke=stroke_num)
        stroke_num = str(stroke_num).split(".")[0]
        selected_filters.append(f'{stroke_num}:Stroke Engines')

    if not selected_filters:
        selected_filters.append('All Bikes')

    """ Search bar Logic """
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            queries = Q(manufacturer__icontains=query) | Q(
                model__icontains=query
            ) | Q(engine_capacity__icontains=query) | Q(
                year__icontains=query
            )
        bikes = bikes.filter(queries)

    context = {
        'bikes': bikes,
        'selected_filters': selected_filters,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to display an inividual products detail """

    bike = get_object_or_404(Bikes, pk=product_id)

    context = {'bike': bike}

    return render(request, 'products/product_detail.html', context)
