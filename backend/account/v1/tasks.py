from celery import shared_task
from account.models import User
from .helpers import send_password_reset_email


@shared_task
def send_password_reset_email_task(user_id: int):
    try:
        user = User.objects.get(pk=user_id)
        send_password_reset_email(user)
    except User.DoesNotExist:
        # silently fail or log
        pass
