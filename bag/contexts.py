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
        item_total = price * quantity
        total_cost += item_total

        # Determine the delivery cost by weight of bike and updated engine capacity
        engine_capacity = item['bike']['engine_capacity']
        bike_with_updated_capacity = Bikes.objects.filter(model=bike.model, engine_capacity=engine_capacity).first()
        if bike_with_updated_capacity:
            weight = bike_with_updated_capacity.weight
            if weight > 100:
                delivery_cost += 155
            elif weight > 90:
                delivery_cost += 100
            else:
                delivery_cost += 90

    # Add delivery cost to the total cost
    grand_total = total_cost + delivery_cost

    # Update the session values
    request.session['total_cost'] = total_cost
    request.session['delivery_cost'] = delivery_cost
    request.session['grand_total'] = grand_total
    print(total_cost)
    print(grand_total)


    # Variables for the engine capacity of a model of a bike
    selected_model = request.session.get('selected_model')
    capacities = Bikes.objects.filter(model=selected_model).values_list('engine_capacity', flat=True).distinct()

    context = {
        'bag': bag,
        'capacities': capacities,
        'total_cost': total_cost,
        'delivery_cost': delivery_cost,
        'grand_total': grand_total,
    }
    return context
