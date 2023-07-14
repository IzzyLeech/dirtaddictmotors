from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
import stripe

from checkout.webhook_handler import StripeWH_Handler


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
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret,
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid Signature
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(content=e, status=400)

    # Retrieve the user ID from the webhook payload or metadata
    user_id = event.data.object.metadata.get('user_id')

    # Retrieve the user object using the user ID
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse("Invalid user.", status=400)

    payload = event['data']['object']
    bag = payload['metadata'].get('bag')

    # Set up a webhool handler
    handler = StripeWH_Handler(request)

    # Map webhookd events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_failed,
    }

    # Get the  webhook type from Stripe
    event_type = event['type']

    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event
    response = event_handler(event, user)
    return response
