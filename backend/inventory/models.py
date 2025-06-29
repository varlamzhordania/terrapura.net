from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

from core.models import BaseModel

User = get_user_model()


class InventoryBase(BaseModel):
    partner = models.ForeignKey(
        'partners.Partner',
        on_delete=models.CASCADE,
        related_name='inventory_bases',
        verbose_name=_('Partner'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Base Name'),
        help_text=_('Name of the inventory location or base.'),
    )
    country = models.ForeignKey(
        'partners.Country',
        on_delete=models.PROTECT,
        related_name='inventory_bases',
        verbose_name=_('Country'),
    )
    region = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Region'),
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Address'),
    )
    contact_person = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Contact Person'),
    )

    class Meta:
        verbose_name = _('Inventory Base')
        verbose_name_plural = _('Inventory Bases')
        unique_together = ('partner', 'name')
        ordering = ['partner', 'name']

    def __str__(self):
        return f"{self.name} ({self.partner.name})"


class InventoryItem(BaseModel):
    herb = models.ForeignKey(
        'herbs.Herb',
        on_delete=models.CASCADE,
        related_name='stock_items',
        verbose_name=_('Herb'),
    )
    base = models.ForeignKey(
        InventoryBase,
        on_delete=models.CASCADE,
        related_name='inventory_items',
        verbose_name=_('Inventory Base'),
    )
    quantity_kg = models.FloatField(
        verbose_name=_('Quantity (kg)'),
        validators=[MinValueValidator(0.01)],
    )
    price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Price per kg (USD)'),
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    currency = models.ForeignKey(
        "checkout.Currency",
        on_delete=models.PROTECT,
        related_name='inventory_items',
        verbose_name=_('Currency'),
    )
    expiration_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Expiration Date'),
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name=_('Available'),
    )
    low_stock_threshold_kg = models.FloatField(
        default=5.0,
        validators=[MinValueValidator(0.1)],
        verbose_name=_('Low Stock Threshold (kg)')
    )

    class Meta:
        verbose_name = _('Inventory Item')
        verbose_name_plural = _('Inventory Items')
        unique_together = ('herb', 'base')
        ordering = ['base', 'herb']

    def __str__(self):
        return f"{self.herb.name} @ {self.base.name} ({self.quantity_kg}kg)"

    def is_below_threshold(self):
        return self.quantity_kg < self.low_stock_threshold_kg


class InventoryTransactionLog(BaseModel):
    class ActionChoices(models.TextChoices):
        ADD = 'add', _('Added Stock')
        REMOVE = 'remove', _('Removed Stock')
        ADJUST = 'adjust', _('Adjusted')
        ORDER = 'order', _('Ordered (Deducted)')

    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    action = models.CharField(max_length=20, choices=ActionChoices.choices)
    quantity_kg = models.FloatField(validators=[MinValueValidator(0.01)])
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Inventory Transaction')
        verbose_name_plural = _('Inventory Transactions')

    def __str__(self):
        return f"{self.action} {self.quantity_kg}kg - {self.inventory_item}"


class LowStockAlert(BaseModel):
    inventory_item = models.OneToOneField(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='low_stock_alert'
    )
    triggered_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Low Stock Alert')
        verbose_name_plural = _('Low Stock Alerts')

    def __str__(self):
        return f"⚠️ Low stock for {self.inventory_item}"


class Order(BaseModel):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PROCESSING = 'processing', _('Processing')
        SHIPPED = 'shipped', _('Shipped')
        DELIVERED = 'delivered', _('Delivered')
        CANCELLED = 'cancelled', _('Cancelled')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('Customer'),
    )
    partner = models.ForeignKey(
        'partners.Partner',
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('Partner'),
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name=_('Status'),
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Total Price'),
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Notes'),
    )
    is_approved_by_customer = models.BooleanField(
        default=False,
        verbose_name=_('Customer Approved'),
        help_text=_('Set to true when the customer confirms delivery.'),
    )
    approved_at = models.DateTimeField(verbose_name=_('Approved at'), blank=True, null=True)
    escrow_released = models.BooleanField(
        default=False,
        verbose_name=_('Escrow Released'),
        help_text=_('Indicates if the payment has been released to the partner wallet.'),
    )
    released_at = models.DateTimeField(verbose_name=_('Released at'), blank=True, null=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Order'),
    )
    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
        verbose_name=_('Inventory Item'),
    )
    quantity_kg = models.FloatField(
        verbose_name=_('Quantity (kg)'),
        validators=[MinValueValidator(0.01)],
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Unit Price'),
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Total Price'),
    )

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
        ordering = ['order']

    def __str__(self):
        return f"{self.inventory_item} x {self.quantity_kg}kg"


class Shipment(BaseModel):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', _('Pending')
        IN_TRANSIT = 'in_transit', _('In Transit')
        DELIVERED = 'delivered', _('Delivered')

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='shipment',
        verbose_name=_('Order'),
    )
    tracking_number = models.CharField(
        verbose_name=_("Shipping Tracking Number"),
        max_length=100,
        blank=True,
        null=True,
    )
    shipped_at = models.DateTimeField(
        verbose_name=_("Shipped At"),
        blank=True,
        null=True
    )
    delivered_at = models.DateTimeField(
        verbose_name=_("Delivered At"),
        blank=True,
        null=True
    )
    carrier = models.CharField(
        verbose_name=_("Carrier"),
        max_length=100,
        blank=True,
        null=True
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=50,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )

    class Meta:
        verbose_name = _('Shipment')
        verbose_name_plural = _('Shipments')

    def __str__(self):
        return f"Shipment for Order #{self.order.id} ({self.get_status_display()})"
