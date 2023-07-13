from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.decorators.http import require_POST
import stripe


@require_POST
@csrf_exempt
def stripe_webhook(request):

    # Retrieve the webhook event JSON from Stripe
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    # Variable Keys
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        event = stripe.Event.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid Signature
        return HttpResponse(content=e, status=400)
    except Exception as e:
        return HttpResponse(content=e, status=400)

    # Set up a webhool handler
    handler = StripeWH_Handler(request)

    # Map webhookd events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handler_payment_intent_succeeded,
        'payment_intent.payment_failed': handle_payment_intent_failed,
    }

    # Get the  webhook type from Stripe
    event_type = event['type']

    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event
    response = event_handler(event)
    return response