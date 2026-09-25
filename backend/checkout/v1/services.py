import logging
from django.db import transaction
from checkout.models import Order, OrderPayment

logger = logging.getLogger(__name__)


def handle_stripe_event(event):
    """Route Stripe webhook events to the right handler."""
    event_type = event.get('type')
    data = event.get('data', {}).get('object', {})

    handlers = {
        'checkout.session.completed': process_checkout_completed,
        'payment_intent.succeeded': process_payment_succeeded,
        'payment_intent.payment_failed': process_payment_failed,
        'charge.refunded': process_charge_refunded,
    }

    handler = handlers.get(event_type)
    if handler:
        try:
            handler(data)
        except Exception as e:
            logger.error(f"Error processing event '{event_type}': {e}", exc_info=True)
            raise
    else:
        logger.info(f"No handler for Stripe event type: {event_type}")


@transaction.atomic
def process_checkout_completed(data):
    """Handle checkout.session.completed event."""
    order_id = data.get('metadata', {}).get('order_id')
    payment_intent_id = data.get('payment_intent')

    if not order_id:
        logger.warning("checkout.session.completed without order_id in metadata.")
        return False

    order = Order.objects.filter(id=order_id).first()
    if not order:
        logger.warning(f"Order with ID {order_id} not found.")
        return False

    payment, created = OrderPayment.objects.get_or_create(
        order=order,
        defaults={
            'amount': order.total_price,
            'currency': order.currency,
            'method': 'Stripe',
            'status': OrderPayment.StatusChoices.PENDING,
        }
    )

    payment.mark_completed(transaction_id=payment_intent_id)

    if order.status == Order.StatusChoices.PAYMENT:
        order.status = Order.StatusChoices.PENDING
        order.save(update_fields=['status'])

    logger.info(f"Order {order_id} payment completed via checkout.session.completed.")
    return True

@transaction.atomic
def process_payment_succeeded(data):
    """Handle payment_intent.succeeded event."""
    order_id = data.get('metadata', {}).get('order_id')

    if not order_id:
        logger.warning("payment_intent.succeeded without order_id in metadata.")
        return False

    order = Order.objects.filter(id=order_id).first()
    if order and order.status == Order.StatusChoices.PAYMENT:
        order.status = Order.StatusChoices.PENDING
        order.save(update_fields=['status'])
        logger.info(f"Order {order_id} marked as COMPLETED via payment_intent.succeeded.")
        return True

    return False

@transaction.atomic
def process_payment_failed(data):
    """Handle payment_intent.payment_failed event."""
    order_id = data.get('metadata', {}).get('order_id')
    failure_message = data.get('last_payment_error', {}).get('message', 'Unknown error')

    if not order_id:
        logger.warning("payment_intent.payment_failed without order_id in metadata.")
        return False

    order = Order.objects.filter(id=order_id).first()
    if order:
        order.status = Order.StatusChoices.PAYMENT
        order.save(update_fields=['status'])
        logger.info(f"Order {order_id} payment failed: {failure_message}")
        return True

    return False

@transaction.atomic
def process_charge_refunded(data):
    """Handle charge.refunded event."""
    payment_intent_id = data.get('payment_intent')

    order_payment = OrderPayment.objects.filter(transaction_id=payment_intent_id).first()
    if order_payment:
        order_payment.status = OrderPayment.StatusChoices.REFUNDED
        order_payment.save(update_fields=['status'])

        order = order_payment.order
        order.status = Order.StatusChoices.CANCELLED
        order.save(update_fields=['status'])

        logger.info(f"Order {order.id} marked as REFUNDED via charge.refunded.")
        return True

    return False
