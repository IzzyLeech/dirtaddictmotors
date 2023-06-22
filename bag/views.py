from django.shortcuts import render, redirect, get_object_or_404, reverse
import json
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder

from products.models import Bikes


def view_bag(request):
    """A view to display the contents of the user's bag"""

    return render(request, 'bag/bag.html')

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
        new_weight = Bikes.objects.filter(model=bike.model, engine_capacity=engine_capacity).values_list('weight', flat=True).first()

        # Update the item in the bag
        bag[str(item_id)]['quantity'] = quantity
        bag[str(item_id)]['bike']['engine_capacity'] = engine_capacity
        bag[str(item_id)]['bike']['price'] = float(new_price)
        bag[str(item_id)]['bike']['weight'] = float(new_weight)

        # Update the bag in the session
        request.session['bag'] = json.dumps(bag)
        request.session['selected_engine_capacity'] = engine_capacity

    # Recalculate the updated total cost, delivery cost, and grand total
    total_cost = 0
    delivery_cost = 0

    for item_id, item in bag.items():
        bike = Bikes.objects.get(pk=item['bike']['id'])
        price = float(item['bike']['price'])
        item_quantity = item['quantity']
        item_total = price * item_quantity
        total_cost += item_total

        print('Price of updated bike', price)
        print(item_quantity)
        print('item total=', item_total)
        print('total=', total_cost)

        weight = item['bike']['weight']
        print('Weight=', weight)
        if weight > 100:
            delivery_cost += 155
        elif weight > 90:
            delivery_cost += 100
        else:
            delivery_cost += 90

    grand_total = total_cost + delivery_cost

    # Update the total_cost, delivery_cost, and grand_total in the session
    request.session['total_cost'] = total_cost
    request.session['delivery_cost'] = delivery_cost
    request.session['grand_total'] = grand_total

    print('Updated Total Cost:', total_cost)
    print('Updated Delivery Cost:', delivery_cost)
    print('Updated Grand Total:', grand_total)

    return redirect('view_bag')
