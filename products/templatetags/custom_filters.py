from django import template

register = template.Library()


@register.filter
def remove_decimal(value):
    try:
        int_value = int(float(value))
        return str(int_value)
    except (ValueError, TypeError):
        return value