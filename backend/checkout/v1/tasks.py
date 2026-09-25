import logging
from celery import shared_task
from .services import (
    process_checkout_completed,
    process_payment_succeeded,
    process_payment_failed,
    process_charge_refunded
)

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def handle_stripe_event_task(self, event_type, data):
    """Celery task to handle Stripe events asynchronously."""
    handlers = {
        'checkout.session.completed': process_checkout_completed,
        'payment_intent.succeeded': process_payment_succeeded,
        'payment_intent.payment_failed': process_payment_failed,
        'charge.refunded': process_charge_refunded,
    }

    handler = handlers.get(event_type)
    if not handler:
        logger.info(f"No handler for Stripe event type: {event_type}")
        return

    try:
        handler(data)
    except Exception as e:
        logger.error(f"Error processing event '{event_type}': {e}", exc_info=True)
        self.retry(exc=e)
