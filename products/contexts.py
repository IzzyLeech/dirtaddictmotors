from django.conf import settings
from .models import Bikes


def nav_category_manufacturers(request):
    manufacturers = Bikes.objects.values('manufacturer').distinct()
    context = {'manufacturers': manufacturers}
    return context


def nav_category_engine_capacity(request):
    engine_capacitys = Bikes.objects.values('engine_capacity').distinct().order_by('engine_capacity')
    context = {'engine_capacitys': engine_capacitys}
    return context


def nav_category_stroke(request):
    strokes = Bikes.objects.values('stroke').distinct()
    context = {'strokes': strokes}
    return context
