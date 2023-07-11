from django.shortcuts import render

from products.models import Bikes

import json
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from cloudinary.models import CloudinaryResource
from django.http import JsonResponse


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, CloudinaryResource):
            return str(obj.url)
        return super().default(obj)


def index(request):
    bikes = Bikes.objects.all()
    return render(request, 'home/index.html')


def faq_view(request):
    return render(request, 'home/faq.html')


def delivery_info(request):
    return render(request, 'home/delivery-info.html')


def get_random_bikes(request):
    random_bikes = Bikes.objects.all()
    random_bikes_data = list(random_bikes.values())

    random_bikes_json = json.dumps(random_bikes_data, cls=CustomJSONEncoder)
    return JsonResponse(random_bikes_json, safe=False)
