from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from account.models import User


def send_password_reset_email(instance: User):
    """
    Helper function to prepare and send the password reset email.
    Can be called directly (sync) or wrapped by a Celery task.
    """
    token = PasswordResetTokenGenerator().make_token(instance)
    uid = urlsafe_base64_encode(force_bytes(instance.pk))
    reset_link = f"{settings.FRONTEND_DOMAIN}/auth/reset-password/{uid}/{token}/"

    subject = "Password Reset Request"
    context = {
        "user": instance,
        "reset_link": reset_link,
        "app_name": "Terrapura",
        "support_email": "support@terrapura.com",
        "logo_url": f"{settings.FRONTEND_DOMAIN}/logo.png",
        "valid_hours": 24,
    }
    text_content = f"Click the link to reset your password: {reset_link}"
    html_content = render_to_string("emails/password_reset.html", context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[instance.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


