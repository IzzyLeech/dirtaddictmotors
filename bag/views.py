from django.shortcuts import render, redirect, get_object_or_404, reverse
import json
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages

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
        quantity = bag[item_id]['quantity']
        messages.success(request, f'Increased quantity of {bike} to {quantity}')
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
        messages.success(request, f'Added {bike} to your bag')

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
        # Retrieve the current item in the bag
        item = bag[str(item_id)]

        # Retrieve the bike instance from the database based on item ID
        bike = Bikes.objects.get(pk=item['bike']['id'])

        # Update the quantity of the current item to the desired quantity
        item['quantity'] = quantity

        if quantity == 0:
            del bag[str(item_id)]
        else:
            # Retrieve the new price and weight based on the updated engine capacity
            updated_bike = Bikes.objects.filter(model=bike.model, engine_capacity=engine_capacity).first()
            if updated_bike:
                # Check if there is another bike with the same model and engine capacity in the bag
                other_bike = None
                for key, value in bag.items():
                    if (
                        key != str(item_id)
                        and value['bike']['model'] == bike.model
                        and value['bike']['engine_capacity'] == engine_capacity
                    ):
                        other_bike = value
                        break

                if other_bike:
                    # Update the quantity of the other bike by adding the quantity of the current item
                    other_bike['quantity'] += item['quantity']
                else:
                    # Update the engine capacity, price, and weight of the current item
                    item['bike']['engine_capacity'] = engine_capacity
                    item['bike']['price'] = float(updated_bike.price)
                    item['bike']['weight'] = float(updated_bike.weight)

    # Update the bag in the session
    request.session['bag'] = json.dumps(bag)
    request.session['selected_engine_capacity'] = engine_capacity
    request.session.modified = True

    # Recalculate the updated total cost, delivery cost, and grand total
    total_cost = 0
    delivery_cost = 0

    for item in bag.values():
        bike = Bikes.objects.get(pk=item['bike']['id'])
        price = float(item['bike']['price'])
        item_quantity = item['quantity']
        item_total = price * item_quantity
        total_cost += item_total

        # Calculate the delivery cost based on the weight of the bike
        weight = bike.weight
        print("Weight:", weight)
        if weight is not None:
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

    return redirect(reverse('view_bag'))
