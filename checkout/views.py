from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from django.views.decorators.http import require_POST
from django.db import transaction

import json
import stripe

from products.models import Bikes
from .models import Order, OrderItem
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from .forms import OrderForm
from bag.contexts import bag_contents


@require_POST
def cache_checkout_data(request):

    bag = json.loads(request.session.get('bag', '{}'))

    for item_id, item in bag.items():
        item['bike'].pop('manufacturer', None)
        item['bike'].pop('model', None)
        item['bike'].pop('engine_capacity', None)
        item['bike'].pop('image_url', None)
        item['bike'].pop('year', None)

    # Convert the modified bag back to a string
    bag_str = json.dumps(bag)

    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': bag_str[:500],
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })

        return HttpResponse(status=200)

    except Exception as e:
        messages.error(
            request,
            'Sorry, your payment cannot be processed right now. '
            'Please try again later.')
        return HttpResponse(content=str(e), status=400)


def checkout_view(request):
    """View that will handle the checkout logic"""

    if not request.user.is_authenticated:
        return redirect(reverse('registration_page'))

    # Stripe key variables
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Retrieve the bag data from the session
    bag_json = request.session.get('bag', '{}')
    bag = json.loads(bag_json)

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
            order_item.subtotal = order_item.subtotal

            # Append the order item to the list
            items.append(order_item)

    user_profile = request.user.userprofile

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
            with transaction.atomic():
                # Create the order instance
                order = Order(
                    user_profile=user_profile,
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
                pid = request.POST.get('client_secret').split('_secret')[0]
                order.stripe_pid = pid
                order.original_bag = json.dumps(bag)
                # Save the order
                order.save()

                # Assign the order to the order items and save them
                for order_item in items:
                    order_item.order = order
                    order_item.save()

                # Calculate the delivery cost
                delivery_cost = sum(
                                order_item.calculate_delivery_cost()
                                for order_item in items)
                order.delivery_cost = delivery_cost

                # Update the grand total using the update_grand_total method
                order.update_grand_total()
                order.payment_status = 'PAID'
                # Save the Order instance again to reflect the updates
                order.save()

                # Save the user's info to the profile if 'save-info' is checked
                if 'save-info' in request.POST and \
                        request.POST['save-info'] == 'on':
                    profile = UserProfile.objects.get(user=request.user)
                    names = form_data['full_name'].split()
                    profile.user.first_name = names[0] \
                        if len(names) > 0 else ""
                    profile.user.last_name = names[1] if len(names) > 1 else ""
                    profile.default_phone_number = order.phone_number
                    profile.default_country = order.country
                    profile.default_postcode = order.postcode
                    profile.default_town_or_city = order.town_or_city
                    profile.default_street_address1 = order.street_address1
                    profile.default_street_address2 = order.street_address2
                    profile.default_county = order.county
                    profile.user.save()
                    profile.save()

            return redirect(
                    reverse('checkout_success', args=[order.order_number]))
    else:
        # Create a Stripe payment intent
        current_bag = bag_contents(request)

        # Validation for checkout page
        if not current_bag:
            messages.error(
                request,
                "There are no items in the bag, "
                "please add an item!")
            return redirect(reverse('products'))

        total = current_bag['grand_total']

        # Ensure the total is at least 1
        if total < 1:
            total = 1

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),
            currency='eur',
            metadata={
                'user_id': request.user.id
            }
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    context = {
        'items': items,
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'user': request.user,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """ View to render a successful checkout"""
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(
        request,
        (
            f'Your Order has been successfully processed {order.user_profile}!'
            f'Your order number is {order.order_number}. A confirmation email '
            f'has been sent to {order.email}'
        )
    )

    if 'bag' in request.session:
        del request.session['bag']

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)
