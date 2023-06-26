from django.shortcuts import render
from django.conf import settings

import json
import stripe


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
        bike_id = item.get('bike_id')  # Use get() method to handle missing key
        if bike_id:
            quantity = item.get('quantity', 0)
            engine_capacity = item.get('engine_capacity', 0)

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
                user=request.user,  # Set the user ID
                full_name=form_data['full_name'],
                email=form_data['email'],
                phone_number=form_data['phone_number'],
                street_address1=form_data['street_address1'],
                street_address2=form_data['street_address2'],
                postcode=form_data['postcode'],
                town_or_city=form_data['town_or_city'],
                county=form_data['county'],
                country=form_data['country'],
            )
            # Save the order
            order.save()
            # Set the delivery cost for the order
            order.calculate_delivery_cost(items)
            # Update the grand total using the update_grand_total method
            order.update_grand_total()

            # Create OrderItem instances for each item in the bag
            for item in items:
                bike = item['bike']
                quantity = item['quantity']

                OrderItem.objects.create(
                    order=order,
                    bike=bike,
                    quantity=quantity,
                    price=bike.price,
                )

    else:
        # Create an empty form if it's a GET request
        order_form = OrderForm()

    context = {
        'items': items,
        'order_form': order_form,
    }

    return render(request, 'checkout/checkout.html', context)
