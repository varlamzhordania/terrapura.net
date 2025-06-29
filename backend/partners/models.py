from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from core.models import BaseModel

User = get_user_model()


class Region(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=100, unique=True)

    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')
        ordering = ('name', 'created_at')

    def __str__(self):
        return f"{self.name}"


class Country(BaseModel):
    name = models.CharField(
        verbose_name=_('Country name'),
        max_length=100,
        unique=True
    )
    iso_code = models.CharField(
        verbose_name=_("ISO Code"),
        max_length=3,
        unique=True
    )
    region = models.ForeignKey(
        Region,
        verbose_name=_("Region"),
        on_delete=models.SET_NULL,
        related_name='countries',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ('name', 'region', 'created_at')

    def __str__(self):
        return self.name


class Partner(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Organization Name'),
        help_text=_('Full name of the organization or business.'),
    )
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='partners')
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Address'),
        help_text=_('Physical or mailing address of the organization.'),
    )
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('Website'),
        help_text=_('Official website URL.'),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Description'),
        help_text=_('Short description of the organization and its offerings.'),
    )
    verified = models.BooleanField(
        default=False,
        verbose_name=_('Verified'),
        help_text=_('Indicates whether this partner is officially verified.'),
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name=_('Average Rating'),
        help_text=_("Aggregate review rating from customers (0.00 to 5.00)."),
    )

    class Meta:
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class PartnerContact(BaseModel):
    class ContactType(models.TextChoices):
        EMAIL = 'email', _('Email')
        PHONE = 'phone', _('Phone')

    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(verbose_name=_('Name'), max_length=255)
    type = models.CharField(
        max_length=10,
        choices=ContactType.choices,
        verbose_name=_('Contact Type'),
        help_text=_('Whether this is an email or phone contact.')
    )
    value = models.CharField(max_length=100, verbose_name=_("Contact Info"))

    class Meta:
        verbose_name = _("Partner Contact")
        verbose_name_plural = _("Partner Contacts")
        unique_together = ('partner', 'type', 'value')
        ordering = ['partner', 'type', 'name']
        indexes = [models.Index(fields=['partner', 'type'])]

    def __str__(self):
        return f"{self.partner.name} ({self.type}: {self.value})"


class PartnerStaff(BaseModel):
    class StaffRoleChoices(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        MANAGER = 'manager', _('Manager')
        VIEWER = 'viewer', _('Viewer')

    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='staff_members',
        verbose_name=_('Partner'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='partner_roles',
        verbose_name=_('User'),
    )
    role = models.CharField(
        max_length=20,
        choices=StaffRoleChoices.choices,
        default=StaffRoleChoices.VIEWER,
        verbose_name=_('Staff Role'),
        help_text=_('Defines permission level within the organization.'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is Active'),
        help_text=_('Whether this staff member currently has access.'),
    )

    class Meta:
        verbose_name = _('Partner Staff')
        verbose_name_plural = _('Partner Staff')
        unique_together = ('partner', 'user')
        ordering = ['partner', 'role']
        indexes = [models.Index(fields=['partner', 'role'])]

    def __str__(self):
        name = self.user.get_full_name() if self.user else _("Unknown User")
        return f"{name} - {self.partner.name if self.partner else _('Unknown Partner')} ({self.get_role_display()})"


class PartnerReview(BaseModel):
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('Partner'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='partner_reviews',
        verbose_name=_('User'),
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name=_('Rating'),
        help_text=_('Rating from 1 to 5 stars.'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Comment'),
        help_text=_('Optional written feedback.'),
    )
    approved = models.BooleanField(
        default=True,
        verbose_name=_('Approved'),
        help_text=_('Whether the review is approved and visible to public.'),
    )

    class Meta:
        verbose_name = _('Partner Review')
        verbose_name_plural = _('Partner Reviews')
        ordering = ['-created_at']
        unique_together = ('partner', 'user')

    def __str__(self):
        return f"{self.user} → {self.partner} ({self.rating})"


class PartnerWallet(BaseModel):
    partner = models.OneToOneField(
        Partner,
        on_delete=models.CASCADE,
        related_name='wallet',
        verbose_name=_('Partner'),
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Balance'),
    )
    currency = models.ForeignKey(
        "checkout.Currency",
        on_delete=models.PROTECT,
        related_name='wallets',
        verbose_name=_('Currency'),
    )

    class Meta:
        verbose_name = _('Partner Wallet')
        verbose_name_plural = _('Partner Wallets')

    def __str__(self):
        return f"{self.partner.name} Wallet - {self.balance} {self.currency.code}"


class WalletTransaction(BaseModel):
    class TransactionType(models.TextChoices):
        CREDIT = 'credit', _('Credit')
        DEBIT = 'debit', _('Debit')

    wallet = models.ForeignKey(
        PartnerWallet,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name=_('Wallet'),
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Amount'),
    )
    type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        verbose_name=_('Transaction Type'),
    )
    purpose = models.CharField(
        max_length=100,
        verbose_name=_('Purpose'),
        help_text=_('Description or reason for this transaction.'),
    )
    reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Reference'),
        help_text=_('Optional external or internal reference.'),
    )

    class Meta:
        verbose_name = _('Wallet Transaction')
        verbose_name_plural = _('Wallet Transactions')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_type_display()} {self.amount} for {self.wallet.partner.name}"
