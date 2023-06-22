from django import template
from products.models import Bikes

register = template.Library()


@register.filter
def get_price(engine_capacity, model):
    price = Bikes.objects.filter(model=model, engine_capacity=engine_capacity).values_list('price', flat=True).first()
    return price