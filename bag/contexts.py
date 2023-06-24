import json
from products.models import Bikes


def bag_contents(request):
    # Receive the content of the bag from the current session
    bag_json = request.session.get('bag', '{}')
    bag = json.loads(bag_json)

    # Variables for cost
    total_cost = 0
    delivery_cost = 0

    # Calculate the items of the bag by the quantity
    for item_id, item in bag.items():
        bike = Bikes.objects.get(pk=item['bike']['id'])
        price = float(item['bike']['price'])
        quantity = item['quantity']
        print("Item ID:", item_id)
        print("Quantity:", quantity)
        item_total = price * quantity
        total_cost += item_total

        # Retrieve the weight from the database based on bike ID and engine capacity
        engine_capacity = item['bike']['engine_capacity']
        weight = Bikes.objects.filter(model=bike.model, engine_capacity=engine_capacity).values_list('weight', flat=True).first()

        if weight is not None:
            weight = float(weight)

            # Update the weight in the bag for the current item
            item['bike']['weight'] = weight

            # Determine the delivery cost by weight of bike
            if weight > 100:
                delivery_cost += 155
            elif weight > 90:
                delivery_cost += 100
            else:
                delivery_cost += 90

        print("Item ID:", item_id)
        print("Quantity:", quantity)

    # Add delivery cost to the total cost
    grand_total = total_cost + delivery_cost

    # Update the session values
    request.session['total_cost'] = total_cost
    request.session['delivery_cost'] = delivery_cost
    request.session['grand_total'] = grand_total

    # Variables for the engine capacity of a model of a bike
    selected_model = request.session.get('selected_model')
    capacities = Bikes.objects.filter(model=selected_model).values_list('engine_capacity', flat=True).distinct()

    # Variable to get the quantity
    total_quantity = sum(item['quantity'] for item in bag.values())
    print("Total Quantity:", total_quantity)

    context = {
        'bag': bag,
        'capacities': capacities,
        'total_cost': total_cost,
        'delivery_cost': delivery_cost,
        'grand_total': grand_total,
        'bag_quantity': total_quantity
    }
    return context
