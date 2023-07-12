from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from decimal import Decimal

import json
import stripe

from products.models import Bikes
from .models import Order, OrderItem
from .forms import OrderForm
from bag.contexts import bag_contents


@login_required
def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse('registration_page'))

    # Stripe key variables
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Retrieve the bag data from the session
    bag_json = request.session.get('bag', '{}')
    bag = json.loads(bag_json)

    # Validation for checkout page
    if not bag:
        messages.error(request, "There are no items in the bag, please add an item!")
        return redirect(reverse('products'))

    # Get the list of items from the bag
    items = []
    order_total = Decimal('0.00')

    for item in bag.values():
        bike_data = item.get('bike')
        bike_id = bike_data.get('id') if bike_data else None
        if bike_id:
            quantity = item.get('quantity', 0)
            engine_capacity = item.get('engine_capacity', 0)

            # Retrieve the bike instance from the database based on bike ID
            bike = Bikes.objects.get(pk=bike_id)

            # Calculate the item total
            item_total = bike.price * quantity
            # Add the item total to the order total
            order_total += item_total

            # Create an instance of OrderItem
            order_item = OrderItem(
                bike=bike,
                quantity=quantity,
                price=bike.price,
            )
            order_item.subtotal = order_item.subtotal()
            print("Order subtotal", order_item.subtotal)

            # Append the order item to the list
            items.append(order_item)

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

            # Calculate the delivery cost for the order
            delivery_cost = sum(item.calculate_delivery_cost() for item in items)
            print("Delivery Cost", delivery_cost)
            order.delivery_cost = delivery_cost

            # Calculate the grand total of the order
            order.grand_total = order_total + delivery_cost

            # Save the Order instance again to reflect the updates
            order.save()
            return redirect(reverse('checkout_success', args=[order.order_number]))
    else:
        # Create a Stripe payment intent
        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        print("Total for stripe", total)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),
            currency='eur',
        )
        print(intent)

        order_form = OrderForm()

    context = {
        'items': items,
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)




def checkout_success(request, order_number):
    """ View to render a successful checkout"""
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Your Order has been successfully processed {order.user}! Your order number is {order.order_number}. A confiramtion email has been sent to {order.email}')

    if 'bag' in request.session:
        del request.session['bag']

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)
