from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe


@csrf_exempt
def stripe_webhook(request):

    # Retrieve the webhook event JSON from Stripe
    payload = request.body
    event = None

    # Variable Keys
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Return a response to acknowledge receipt of the event
    return HttpResponse(status=200)