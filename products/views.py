from django.shortcuts import render
from .models import Bikes


def products_display(request):
    """View to display all products"""

    bikes = Bikes.objects.all()

    context = {
        'bikes': bikes,
        }
    return render(request, 'products/products.html', context)


def products_by_manufacturer(request, manufacturer_name):
    # Retrieve bikes for the specified manufacturer name
    bikes = Bikes.objects.filter(manufacturer=manufacturer_name)

    context = {
        'bikes': bikes,
        'manufacturer_name': manufacturer_name,
    }
    return render(request, 'products/products.html', context)
