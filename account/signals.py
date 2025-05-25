import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

logger = logging.getLogger(__name__)

User = get_user_model()


@receiver(user_logged_in, sender=User)
def update_last_ip_address(sender, request, user, **kwargs):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR')

    if not ip_address:
        logger.warning(f"User {user.username} logged in, but no IP address found in request.")
        return

    if user.last_ip != ip_address:
        user.last_ip = ip_address
        user.save(update_fields=['last_ip'])

        logger.info(f"User {user.username} IP address updated to {ip_address}.")
    else:
        logger.info(f"User {user.username} logged in from the same IP address: {ip_address}.")
