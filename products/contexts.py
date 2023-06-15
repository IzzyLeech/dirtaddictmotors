from django.conf import settings
from .models import Bikes


def nav_category_manufacturers(request):
    manufacturers = Bikes.objects.values('manufacturer').distinct()
    context = {'manufacturers': manufacturers}
    return context



def nav_category_engine_capacity(request):
    engine_capacitys = Bikes.objects.values_list('engine_capacity', flat=True).distinct()
    context = {'engine_capacitys': engine_capacitys}
    return context


def nav_category_stroke(request):
    strokes = Bikes.objects.values_list('stroke', flat=True).distinct()
    context = {'strokes': strokes}
    return context
