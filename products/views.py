from django.shortcuts import render
from .models import Bikes


def products_display(request):
    """View to display products with filter option for certain option"""

    bikes = Bikes.objects.all()

    context = {
        'bikes': bikes,
        }
    return render(request, 'products/products.html', context)
