from django import template
from products.models import Bikes

register = template.Library()


@register.filter
def get_price(engine_capacity, model):
    price = Bikes.objects.filter(
                model=model,
                engine_capacity=engine_capacity,
                ).values_list('price', flat=True).first()
    return price


@register.simple_tag(takes_context=True)
def get_bag_quantity(context):
    request = context['request']
    bag = request.session.get('bag', {})
    total_quantity = sum(item['quantity'] for item in bag.values())
    return total_quantity


@register.filter
def calc_multiply(value, arg):
    return value * arg
