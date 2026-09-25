import logging
import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_KEY
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        logger.error(f"Stripe webhook error: {e}")
        return HttpResponseBadRequest()

    event_type = event.get("type")
    data = event.get("data", {}).get("object", {})

    # Send to Celery
    from .tasks import handle_stripe_event_task
    handle_stripe_event_task.delay(event_type, data)

    return HttpResponse(status=200)

