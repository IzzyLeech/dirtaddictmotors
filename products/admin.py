from django.contrib import admin
from .models import Bikes


class BikeAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'manufacturer',
        'model',
        'year',
        'engine_capacity',
        'stroke',
        'speed',
        'price',
    )

    ordering = ('sku')


admin.site.register(Bikes)
