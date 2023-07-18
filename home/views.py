from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import user_passes_test
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.db.models import CharField
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.conf import settings

from products.models import Bikes
from .forms import SubscriberForm
from checkout.models import Order

import json
from decimal import Decimal

from cloudinary.models import CloudinaryResource


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, CloudinaryResource):
            return str(obj.url)
        return super().default(obj)


def index(request):
    bikes = Bikes.objects.all()
    return render(request, 'home/index.html')


def faq_view(request):
    return render(request, 'home/faq.html')


def delivery_info(request):
    return render(request, 'home/delivery-info.html')


def newsletter_signup(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            subscriber = form.save()

            # Send confirmation email
            subject = 'Newsletter Subscription Confirmation'
            message = 'Thank you for subscribing to our newsletter!'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [subscriber.email]

            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                print(f"An error occurred while sending the email: {str(e)}")

            messages.success(
                request,
                'You have successfully subscribed to our newsletter!')
            return redirect(reverse('home'))
    else:
        form = SubscriberForm()
    return render(request, 'home/newsletter.html', {'form': form})


def superuser_check(user):
    return user.is_superuser


@user_passes_test(superuser_check)
def admin_view(request):
    if not request.user.is_superuser:
        messages.error(request, 'Restricted Area')
        return redirect(reverse('home'))

    orders = Order.objects.all().order_by('-date')
    payment_status_choices = dict(
        CharField(choices=Order._meta.get_field('payment_status').choices)
        .flatchoices)

    context = {
        'orders': orders,
        'payment_status_choices': payment_status_choices}
    return render(request, 'home/admin_orders.html', context)


def update_payment_status(request, order_id):
    if request.method == 'POST':
        payment_status = request.POST.get('payment_status')
        order = Order.objects.get(id=order_id)
        order.payment_status = payment_status
        order.save()
        messages.info(
            request,
            f"The payment status for order {order.order_number} \
            has been updated to {payment_status}.")
    return redirect(reverse('admin-orders'))


def get_random_bikes(request):
    random_bikes = Bikes.objects.all()
    random_bikes_data = list(random_bikes.values())

    random_bikes_json = json.dumps(random_bikes_data, cls=CustomJSONEncoder)
    return JsonResponse(random_bikes_json, safe=False)
