from django.contrib import admin

from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('price',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)

    readonly_fields = ('order_number', 'date', 'delivery_cost',
                       'order_total', 'grand_total'
                       )

    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'street_address1',
              'street_address2', 'postcode', 'town_or_city',
              'county', 'country', 'payment_status',
              'delivery_cost', 'order_total', 'grand_total'
              )

    list_display = ('order_number', 'date', 'full_name',
                    'payment_status', 'delivery_cost',
                    'order_total', 'grand_total')

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)

