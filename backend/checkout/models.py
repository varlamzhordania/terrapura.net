from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from core.models import BaseModel

User = get_user_model()


class Currency(BaseModel):
    code = models.CharField(
        verbose_name=_('Currency code'),
        max_length=10,
        unique=True,
        help_text=_('The currency code, e.g. USD, EUR'),
    )
    name = models.CharField(
        verbose_name=_('Currency name'),
        max_length=100,
        help_text=_('The currency name, e.g. United States Dollar, European Euro'),
    )
    symbol = models.CharField(
        verbose_name=_('Currency symbol'),
        max_length=10,
        help_text=_('The currency symbol, e.g. $'),
    )

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')
        ordering = ['code']

    def __str__(self):
        return f"{self.code} ({self.symbol})"


class ExchangeRate(BaseModel):
    base_currency = models.ForeignKey(
        Currency,
        related_name='base_rates',
        on_delete=models.CASCADE,
        verbose_name=_('Base Currency'),
    )
    target_currency = models.ForeignKey(
        Currency,
        related_name='target_rates',
        on_delete=models.CASCADE,
        verbose_name=_('Target Currency'),
    )
    rate = models.DecimalField(
        verbose_name=_('Exchange Rate'),
        max_digits=12,
        decimal_places=6,
        help_text=_('Rate to convert 1 unit of base currency to target currency.'),
    )

    class Meta:
        verbose_name = _('Exchange Rate')
        verbose_name_plural = _('Exchange Rates')
        unique_together = ('base_currency', 'target_currency')
        ordering = ['base_currency', 'target_currency']

    def __str__(self):
        return f"1 {self.base_currency.code} = {self.rate} {self.target_currency.code}"


class ShoppingCart(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name=_('User'),
    )
    partner = models.ForeignKey(
        'partners.Partner',
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name=_('Partner'),
    )

    class Meta:
        verbose_name = _('Shopping Cart')
        verbose_name_plural = _('Shopping Carts')
        unique_together = ('user', 'partner')
        ordering = ['-created_at']

    def __str__(self):
        return f"Cart #{self.id} for {self.user.username}"


class ShoppingCartItem(BaseModel):
    cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Shopping Cart'),
    )
    inventory_item = models.ForeignKey(
        'inventory.InventoryItem',
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name=_('Inventory Item'),
    )
    quantity_kg = models.FloatField(
        verbose_name=_('Quantity (kg)'),
        help_text=_('The quantity of the item in kilograms.'),
    )

    class Meta:
        verbose_name = _('Shopping Cart Item')
        verbose_name_plural = _('Shopping Cart Items')
        unique_together = ('cart', 'inventory_item')
        ordering = ['cart', 'created_at']

    def __str__(self):
        return f"{self.inventory_item} x {self.quantity_kg}kg"


class Payment(BaseModel):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SUCCESSFUL = 'successful', _('Successful')
        FAILED = 'failed', _('Failed')

    order = models.OneToOneField(
        'inventory.Order',
        on_delete=models.CASCADE,
        related_name='payment',
        verbose_name=_('Order'),
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Amount'),
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name=_('Currency'),
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name=_('Status'),
    )
    method = models.CharField(
        max_length=50,
        verbose_name=_('Payment Method'),
        help_text=_('e.g. Stripe, Wallet, PayPal'),
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Transaction ID'),
    )
    paid_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Paid At'),
    )

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.get_status_display()}"
