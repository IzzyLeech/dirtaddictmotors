from django.shortcuts import render, redirect, get_object_or_404, reverse
import json
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder

from products.models import Bikes


def view_bag(request):
    """A view to display the contents of the user's bag"""

    bag_json = request.session.get('bag', '{}')
    bag = json.loads(bag_json)

    total_cost = float(request.session.get('total_cost', 0))
    bike_models = set(item['bike']['model'] for item in bag.values())

    for item_id, item in bag.items():
        bike = Bikes.objects.get(pk=item['bike']['id'])
        price = float(bike.price)
        quantity = item['quantity']
        item_total = price * quantity
        total_cost += item_total

    selected_model = request.session.get('selected_model')
    capacities = Bikes.objects.filter(model=selected_model).values_list('engine_capacity', flat=True).distinct()

    context = {
        'bag': bag,
        'total_cost': total_cost,
        'bike_models': bike_models,
        'capacities': capacities,
    }

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
        engine_capacity = str(bike.engine_capacity)  # Convert engine_capacity to a string

        # Add the product to the bag with an initial quantity of 1
        bag[item_id] = {
            'quantity': 1,
            'bike': {
                'id': bike.id,
                'manufacturer': bike.manufacturer,
                'model': bike.model,
                'price': price,
                'engine_capacity': engine_capacity,
            }
        }

    request.session['selected_model'] = bike.model

    # Update the bag in the session
    request.session['bag'] = json.dumps(bag)

    return redirect(reverse('view_bag'))


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


def adjust_bag_content(request, item_id):
    """A function that adjusts the quantity and engine capacity of a product in the bag"""

    # Retrieve the new quantity and engine capacity from the request
    quantity = int(request.POST.get('quantity'))
    engine_capacity = request.POST.get('engine_capacity')

    # Get the user's bag from the session
    bag_json = request.session.get('bag', '{}')
    bag = json.loads(bag_json)

    # Check if the item ID exists in the bag
    if str(item_id) in bag:
        # Retrieve the bike instance from the database based on item ID
        bike = Bikes.objects.get(pk=bag[str(item_id)]['bike']['id'])

        # Retrieve the new price based on the updated engine capacity
        new_price = Bikes.objects.filter(model=bike.model, engine_capacity=engine_capacity).values_list('price', flat=True).first()

        # Update the quantity and engine capacity of the item in the bag
        bag[str(item_id)]['quantity'] = quantity
        bag[str(item_id)]['bike']['engine_capacity'] = engine_capacity
        bag[str(item_id)]['bike']['price'] = float(new_price)

        # Update the bag in the session
        request.session['bag'] = json.dumps(bag)

    # Recalculate the updated total cost
    total_cost = sum(
        float(item['bike']['price']) * item['quantity']
        for item_id, item in bag.items()
    )

    # Update the total_cost in the session
    request.session['total_cost'] = total_cost

    return redirect('view_bag')
