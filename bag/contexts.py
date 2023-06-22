import json
from products.models import Bikes


def bag_contents(request):
    # Receieve the content of the bag from the current session
    bag_json = request.session.get('bag', '{}')
    bag = json.loads(bag_json)

    # Variables for cost
    total_cost = 0
    delivery_cost = 0

    # Calualte the items of the bag by the quantity
    for item_id, item in bag.items():
        bike = Bikes.objects.get(pk=item['bike']['id'])
        price = float(bike.price)
        quantity = item['quantity']
        item_total = price * quantity
        total_cost += item_total

    # Determine the deleivery cost by weight of bike
        weight = bike.weight
        if weight > 100:
            delivery_cost += 155
        elif weight > 90:
            delivery_cost += 100
        else:
            delivery_cost += 90

    # Add delivery cost to the total cost
    grand_total = total_cost + delivery_cost

    # Variables for the engine caacity of a model of a bike
    selected_model = request.session.get('selected_model')
    capacities = Bikes.objects.filter(model=selected_model).values_list('engine_capacity', flat=True).distinct()

    context = {
        'bag': bag,
        'total_cost': total_cost,
        'capacities': capacities,
        'delivery_cost': delivery_cost,
        'grand_total': grand_total,
    }
    return context