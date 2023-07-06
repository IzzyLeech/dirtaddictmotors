from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.contrib import messages

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

    sort_param = request.GET.get('sort')
    default_sort = request.GET.get('sort', 'manufacturer')

    if sort_param == 'year':
        bikes = bikes.order_by('-year')
        default_sort = 'year'
    elif sort_param == '-year':
        bikes = bikes.order_by('year')
        default_sort = '-year'
    elif sort_param == 'price':
        bikes = bikes.order_by('-price')
        default_sort = 'price'
    elif sort_param == '-price':
        bikes = bikes.order_by('price')
        default_sort = '-price'
    elif sort_param == 'manufacturer':
        bikes = bikes.order_by('manufacturer')
        default_sort = 'manufacturer'
    elif sort_param == '-manufacturer':
        bikes = bikes.order_by('-manufacturer')
        default_sort = '-manufacturer'

    # Search bar Logic
    query = request.GET.get('q')
    if query:
        bikes = bikes.filter(
            Q(manufacturer__icontains=query) |
            Q(model__icontains=query) |
            Q(engine_capacity__icontains=query) |
            Q(year__icontains=query)
        )
        selected_filters = [f'Search result for "{query}"']
    else:
        messages.warning(request, 'Please enter a search query.')

    paginator = Paginator(bikes, 8)
    page_number = request.GET.get('page')
    bikes_page = paginator.get_page(page_number)

    context = {
        'bikes': bikes_page,
        'selected_filters': selected_filters,
        'default_sort': default_sort,
        'query': query,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to display an inividual products detail """

    bike = get_object_or_404(Bikes, pk=product_id)

    context = {'bike': bike}

    return render(request, 'products/product_detail.html', context)
