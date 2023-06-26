from django.shortcuts import render
from django.conf import settings
from decimal import Decimal

import json
import stripe

from products.models import Bikes
from .models import Order, OrderItem
from .forms import OrderForm


def checkout_view(request):
    # Retrieve the bag data from the session
    bag_json = request.session.get('bag', '{}')
    bag = json.loads(bag_json)

    # Get the list of items from the bag
    items = []
    order_total = Decimal('0.00')

    for item in bag.values():
        bike_data = item.get('bike')
        bike_id = bike_data.get('id') if bike_data else None
        print("bike_id:", bike_id)
        if bike_id:
            quantity = item.get('quantity', 0)
            print('Quantity', quantity)
            engine_capacity = item.get('engine_capacity', 0)
            print("Engine", engine_capacity)

            # Retrieve the bike instance from the database based on bike ID
            bike = Bikes.objects.get(pk=bike_id)

            # Calculate the item total
            item_total = bike.price * quantity

            # Add the item total to the order total
            order_total += item_total
            print(f"Order total:", order_total)

            # Create an instance of OrderItem
            order_item = OrderItem(
                bike=bike,
                quantity=quantity,
                price=bike.price,
            )

            # Append the order item to the list
            items.append(order_item)

    # Calculate the total weight of all the bikes in the items list
    total_weight = sum(item.bike.weight for item in items)

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        # Data from the form when submitted
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'country': request.POST['country'],
        }
        # Form Variable
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            # Create the order instance
            order = Order(
                user=request.user,
                full_name=form_data['full_name'],
                email=form_data['email'],
                phone_number=form_data['phone_number'],
                street_address1=form_data['street_address1'],
                street_address2=form_data['street_address2'],
                postcode=form_data['postcode'],
                town_or_city=form_data['town_or_city'],
                county=form_data['county'],
                country=form_data['country'],
                order_total=order_total,
            )
            # Save the order
            order.save()

            # Assign the order to the order items and save them
            for order_item in items:
                order_item.order = order
                order_item.save()

            # Calculate the delivery cost
            order.calculate_delivery_cost(items)

            # Update the grand total using the update_grand_total method
            order.update_grand_total()

            # Save the Order instance again to reflect the updates
            order.save()

    else:
        order_form = OrderForm()

    context = {
        'items': items,
        'order_form': order_form,
    }

    return render(request, 'checkout/checkout.html', context)
