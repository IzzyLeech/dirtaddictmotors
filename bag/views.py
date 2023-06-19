from django.shortcuts import render, redirect, get_object_or_404
import json
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder

from products.models import Bikes


def view_bag(request):
    """ A view to display the contents of the user bag """

    bag_json = request.session.get('bag', '{}')
    bag = json.loads(bag_json)

    print(bag)

    total_cost = 0

    for item_id, item in bag.items():
        bike = Bikes.objects.get(pk=item['bike']['id'])
        price = float(bike.price)
        quantity = item['quantity']
        item_total = price * quantity
        total_cost += item_total

        print(total_cost)

    context = {'bag': bag, 'total_cost': total_cost}

    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_id):
    """A function that adds a product to the bag"""

    # Retrieve the bike based on the provided item_id
    bike = get_object_or_404(Bikes, id=int(item_id))

    # Get the user's bag from the session or create an empty bag if it doesn't exist
    bag_json = request.session.get('bag', '{}')
    bag = json.loads(bag_json)

    # Check if the product is already in the bag
    if item_id in bag:
        # Increment the quantity by 1
        bag[item_id]['quantity'] += 1
    else:
        # Convert Decimal fields to float
        price = float(bike.price)

        # Add the product to the bag with an initial quantity of 1
        bag[item_id] = {
            'quantity': 1,
            'bike': {
                'id': bike.id,
                'manufacturer': bike.manufacturer,
                'model': bike.model,
                'engine_capacity': bike.engine_capacity,
                'price': price,
            }
        }

    # Update the bag in the session
    request.session['bag'] = json.dumps(bag, cls=DjangoJSONEncoder)

    # Redirect the user to the bag page
    return redirect('view_bag')


def remove_from_bag(request, item_id):
    """A function that removes a bike from the bag"""

    # Get the user's bag from the session
    bag = request.session.get('bag', {})

    # Convert the bag to a dictionary if it's a string
    if isinstance(bag, str):
        bag = json.loads(bag)

    # Check if the bike is in the bag
    if item_id in bag:
        del bag[item_id]  # Remove the bike from the bag

        # Update the bag in the session
        request.session['bag'] = json.dumps(bag, cls=DjangoJSONEncoder)

    # Redirect the user to the bag page
    return redirect('view_bag')