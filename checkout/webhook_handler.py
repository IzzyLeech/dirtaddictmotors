from django.http import HttpResponse
from .models import Order, OrderItem
from products.models import Bikes
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

import logging
import json
import time
import stripe
import ast


class StripeWH_Handler:
    """Handle Stripe Webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event, user_profile=None):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event, user_profile=None):
        """
        Handle the payment_intent.succeeded
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        bag = bag.strip('"\'')
        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        if user_profile is None:
            # Return an error response when user_profile is None
            return HttpResponse("Invalid user profile.", status=400)

        if user_profile is None or isinstance(user_profile, AnonymousUser):
            # Return an error response for anonymous user or when user is None
            return HttpResponse("Invalid user.", status=400)

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

            order = Order.objects.filter(stripe_pid=pid).first()

            if order:
                self._send_confirmation_email(order)
                return HttpResponse(
                    content=f'Webhook received: '
                    '{event["type"]} | SUCCESS: Verified '
                    'order already in database',
                    status=200
                )

            # Create a new order using the received data
            order = Order(
                full_name=shipping_details.name,
                email=billing_details.email,
                phone_number=shipping_details.phone,
                country=shipping_details.address.country,
                postcode=shipping_details.address.postal_code,
                town_or_city=shipping_details.address.city,
                street_address1=shipping_details.address.line1,
                street_address2=shipping_details.address.line2,
                county=shipping_details.address.state,
                grand_total=grand_total,
                original_bag=bag,
                stripe_pid=pid,
                user_profile=user_profile
            )
            order.save()

            bag_dict = {}
            bag = bag.replace("\\", "")
            bag_dict = eval(bag)

            order_items = []
            try:
                for item in bag_dict.values():
                    bike_data = item.get('bike')
                    bike_id = bike_data.get('id') if bike_data else None
                    if bike_id:
                        quantity = item.get('quantity', 0)
                        engine_capacity = item.get('engine_capacity', 0)

                        # Retrieve the bike instance from
                        # the database based on bike ID
                        bike = Bikes.objects.get(pk=bike_id)

                        # Create an instance of OrderItem
                        order_item = OrderItem(
                            bike=bike,
                            quantity=quantity,
                            price=bike.price,
                            order=order
                        )
                        order_item.save()
                        order_items.append(order_item)
            except Exception as e:
                return HttpResponse(
                    content=f'Webhook received: '
                    '{event["type"]} | ERROR: {str(e)}',
                    status=500)

            # Calculate the delivery cost
            delivery_cost = sum(
                order_item.calculate_delivery_cost()
                for order_item in order_items)
            order.delivery_cost = delivery_cost

            # Update the grand total using the update_grand_total method
            order.update_grand_total()

            # Save the Order instance again to reflect the updates
            order.save()

            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received:'
                '{event["type"]} | SUCCESS: Created order in webhook',
                status=200
            )

    def handle_payment_intent_failed(self, event, user_profile=None):
        """
        Handle the payment_intent.failed
        """
        intent = event.data.object
        pid = intent.id
        failure_reason = intent.last_payment_error.get('message')

        # Log the details of the failed payment intent
        logger = logging.getLogger('payment')
        logger.error(f'Payment intent failed. \
            ID: {pid}, Reason: {failure_reason}')

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
