from django.shortcuts import render

import json

from products.models import Bikes
from .models import Order
from .forms import OrderForm


def checkout_view(request):
    # Retrieve the bag data from the session
    bag_json = request.session.get('bag', '{}')
    bag = json.loads(bag_json)

    # Get the list of items from the bag
    items = []
    for item in bag.values():
        bike_id = item['bike']['id']
        quantity = item['quantity']
        engine_capacity = item['bike']['engine_capacity']

        # Retrieve the bike instance from the database based on bike ID
        bike = Bikes.objects.get(pk=bike_id)

        # Create a dictionary for the item
        item_data = {
            'bike': bike,
            'quantity': quantity,
            'engine_capacity': engine_capacity,
        }

        # Add the item to the list
        items.append(item_data)

    # Form Variable
    order_form = OrderForm()

    # Context tags
    context = {
        'items': items,
        'order_form': order_form,

    }

    return render(request, 'checkout/checkout.html', context)