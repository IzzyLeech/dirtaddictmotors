from django.shortcuts import render
from .models import Bikes


def products_display(request, manufacturer_name=None, engine_num=None, stroke_num=None):
    """View to display products based on optional filters"""

    bikes = Bikes.objects.all()

    if manufacturer_name:
        bikes = bikes.filter(manufacturer=manufacturer_name)

    if engine_num:
        bikes = bikes.filter(engine_capacity=engine_num)

    if stroke_num:
        bikes = bikes.filter(stroke=stroke_num)

    context = {
        'bikes': bikes,
    }

    return render(request, 'products/products.html', context)
