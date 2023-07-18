from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from .forms import BikeForm
from .models import Bikes


def products_view(request, manufacturer_name=None, engine_num=None, stroke_num=None):
    """View to display products based on optional filters"""
    bikes = Bikes.objects.all()
    selected_filters = []

    if manufacturer_name:
        bikes = bikes.filter(manufacturer=manufacturer_name)\
            .order_by('engine_capacity')
        selected_filters.append(f'Manufacturer: {manufacturer_name}')
    if engine_num:
        bikes = bikes.filter(engine_capacity=engine_num)
        engine_num = str(engine_num).split(".")[0]
        selected_filters.append(f'Engine Capacity: {engine_num} CC')
    if stroke_num:
        bikes = bikes.filter(stroke=stroke_num).order_by('engine_capacity')
        stroke_num = str(stroke_num).split(".")[0]
        selected_filters.append(f'{stroke_num}:Stroke Engines')

    if not selected_filters:
        selected_filters.append('All Bikes')

    sort_param = request.GET.get('sort')

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
    else:
        bikes = bikes.order_by('manufacturer')
        default_sort = 'default'

    # Search bar Logic
    query = request.GET.get('q')
    if query:
        bikes = bikes.filter(
            Q(manufacturer__icontains=query) |
            Q(model__icontains=query) |
            Q(engine_capacity__icontains=query) |
            Q(year__icontains=query) | Q(starter__icontains=query)
        )
        selected_filters = [f'Search result for "{query}"']

    if request.method == 'GET' and not query and 'submit' in request.GET:
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


def superuser_check(user):
    return user.is_superuser


@user_passes_test(superuser_check)
def add_bike(request):
    """
    Add a bike to the Website
    """
    if not request.user.is_superuser:
        messages.error(request, 'Restricted Area')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = BikeForm(request.POST, request.FILES)
        if form.is_valid():
            bike = form.save()
            messages.success(request, 'The bike has been added to the store')
            return redirect(reverse('product_detail', args=[bike.id]))
        else:
            messages.error(
                request,
                'Error in form, please ensure data is correct')
    else:
        form = BikeForm()

    context = {
        'form': form
    }
    return render(request, 'products/add_bike.html', context)


@user_passes_test(superuser_check)
def edit_bike(request, product_id):
    """
    Edit a bike in the website
    """
    if not request.user.is_superuser:
        messages.error(request, 'Restricted Area')
        return redirect(reverse('home'))

    bike = get_object_or_404(Bikes, id=product_id)
    if request.method == 'POST':
        form = BikeForm(request.POST, request.FILES, instance=bike)
        if form.is_valid():
            form.save()
            messages.success(request, 'The bike has been updated')
            return redirect(reverse('product_detail', args=[bike.id]))
        else:
            messages.error(request, 'Failed to update Bike')
    else:
        form = BikeForm(instance=bike)
        messages.info(request, f'{bike} is being edited')

    context = {
        'form': form,
        'bike': bike
    }
    return render(request, 'products/edit_bike.html', context)


@user_passes_test(superuser_check)
def delete_bike(request, product_id):
    """
    Delete bikes from the website
    """
    if not request.user.is_superuser:
        messages.error(request, 'Restricted Area')
        return redirect(reverse('home'))

    bike = get_object_or_404(Bikes, id=product_id)
    bike.delete()
    messages.success(request, 'The Bike has been deletd from the website')
    return redirect(reverse('products'))
