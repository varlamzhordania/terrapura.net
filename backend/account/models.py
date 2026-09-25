from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

from core.models import BaseModel


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        # extra_fields.setdefault('username', email.split('@')[0])
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField(
        _("email address"),
        unique=True,
        editable=False
    )
    phone_number = PhoneNumberField(
        _("phone number"),
        editable=True,
        blank=True,
        null=True
    )
    last_ip = models.GenericIPAddressField(
        _("Last IP Address"),
        null=True,
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if not self.first_name and not self.last_name:
            return self.email
        return f"{self.first_name} {self.last_name}"


class Address(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name=_('User')
    )
    full_name = models.CharField(
        max_length=150,
        verbose_name=_('Full Name'),
        help_text=_('Name of the recipient for this address'),
    )
    phone_number = PhoneNumberField(
        verbose_name=_('Phone Number'),
        blank=True,
        null=True,
        help_text=_('Contact phone number'),
    )
    line1 = models.CharField(
        max_length=255,
        verbose_name=_('Address Line 1'),
        help_text=_('Street address, P.O. box, company name, c/o'),
    )
    line2 = models.CharField(
        max_length=255,
        verbose_name=_('Address Line 2'),
        blank=True,
        null=True,
        help_text=_('Apartment, suite, unit, building, floor, etc.'),
    )
    city = models.CharField(
        max_length=100,
        verbose_name=_('City / Town'),
    )
    state = models.CharField(
        max_length=100,
        verbose_name=_('State / Province / Region'),
        blank=True,
        null=True,
    )
    postal_code = models.CharField(
        max_length=20,
        verbose_name=_('Postal / Zip Code'),
    )
    country = models.CharField(
        max_length=100,
        verbose_name=_('Country'),
        help_text=_('Country name or ISO code'),
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name=_('Default Address'),
        help_text=_('Designate this as the default delivery address'),
    )

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        ordering = ['-is_default', '-updated_at']

    def __str__(self):
        return f"{self.full_name}, {self.line1}, {self.city}, {self.country}"
