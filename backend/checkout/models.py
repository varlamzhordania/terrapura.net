from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.models import BaseModel, UploadPath

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
        help_text=_(
            'The currency name, e.g. United States Dollar, European Euro'
        ),
    )
    symbol = models.CharField(
        verbose_name=_('Currency symbol'),
        max_length=10,
        help_text=_('The currency symbol, e.g. $'),
    )
    is_base_currency = models.BooleanField(
        default=False,
        verbose_name=_('Currency is base?(systemic)')
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
        help_text=_(
            'Rate to convert 1 unit of base currency to target currency.'
        ),
    )

    class Meta:
        verbose_name = _('Exchange Rate')
        verbose_name_plural = _('Exchange Rates')
        unique_together = ('base_currency', 'target_currency')
        ordering = ['base_currency', 'target_currency']

    def __str__(self):
        return f"1 {self.base_currency.code} = {self.rate} {self.target_currency.code}"


class PaymentMethod(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Name"),
        help_text=_(
            "Name of the payment method, e.g., Stripe, PayPal, Wallet"
        )
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Code"),
        help_text=_("Short code identifier, e.g., stripe, paypal, wallet")
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Optional description for the payment method")
    )
    icon = models.ImageField(
        upload_to=UploadPath(folder="public", sub_path="images"),
        blank=True,
        null=True,
        verbose_name=_("Icon"),
        help_text=_("Optional for payment method icon/logo")
    )
    min_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Minimum amount"),
        help_text=_(
            "Minimum order total required to use this payment method"
        )
    )
    min_currency = models.ForeignKey(
        Currency,
        verbose_name=_("Min amount currency"),
        related_name='payment_methods',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_(
            "Currency the minimum amount is defined in (e.g., EUR, USD)"
        )
    )

    class Meta:
        verbose_name = _("Payment Method")
        verbose_name_plural = _("Payment Methods")
        ordering = ['name']

    def __str__(self):
        return self.name


class ShoppingCart(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name=_('User'),
    )

    class Meta:
        verbose_name = _('Shopping Cart')
        verbose_name_plural = _('Shopping Carts')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Cart for {self.user.get_full_name()}"


class ShoppingCartItem(BaseModel):
    cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Shopping Cart'),
    )
    inventory_item = models.ForeignKey(
        'inventory.InventoryItem',
        on_delete=models.PROTECT,
        related_name='cart_items',
        verbose_name=_('Inventory Item'),
    )
    inventory_price = models.ForeignKey(
        'inventory.InventoryPrice',
        on_delete=models.PROTECT,
        related_name='cart_items',
        verbose_name=_('Inventory Price'),
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name=_('Quantity'),
        help_text=_('The quantity of the item in the price unit.'),
    )

    class Meta:
        verbose_name = _('Shopping Cart Item')
        verbose_name_plural = _('Shopping Cart Items')
        unique_together = ('cart', 'inventory_item', 'inventory_price')
        ordering = ['cart', 'created_at']
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['inventory_item']),
            models.Index(fields=['inventory_price']),
            models.Index(
                fields=['cart', 'inventory_item', 'inventory_price']
            ),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.inventory_item} x {self.quantity}{self.inventory_price.unit}"


class Order(BaseModel):
    class StatusChoices(models.TextChoices):
        PAYMENT = 'payment', _('Payment')
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
    delivery_address = models.ForeignKey(
        "account.Address",
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Delivery Address'),
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PAYMENT,
        verbose_name=_('Status'),
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        verbose_name=_('Total Price'),
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        null=True,
        related_name='orders',
        verbose_name=_('Currency'),
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
    approved_at = models.DateTimeField(
        verbose_name=_('Approved at'),
        blank=True,
        null=True
    )
    escrow_released = models.BooleanField(
        default=False,
        verbose_name=_('Escrow Released'),
        help_text=_(
            'Indicates if the payment has been released to the partner wallet.'
        ),
    )
    released_at = models.DateTimeField(
        verbose_name=_('Released at'),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_approved_by_customer']),
            models.Index(fields=['escrow_released']),
        ]

    def __str__(self):
        return f"Order #{self.id} - {self.user.get_full_name()}"


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Order'),
    )
    inventory_item = models.ForeignKey(
        'inventory.InventoryItem',
        on_delete=models.PROTECT,
        null=True,
        related_name='order_items',
        verbose_name=_('Inventory Item'),
    )
    inventory_price = models.ForeignKey(
        'inventory.InventoryPrice',
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name=_('Inventory Price'),
        null=True,
    )
    quantity = models.DecimalField(
        verbose_name=_('Quantity'),
        max_digits=10,
        decimal_places=4,
        validators=[MinValueValidator(0.0001)],
        default=0.0001,
    )
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        verbose_name=_('Unit Price'),
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        verbose_name=_('Total Price'),
    )

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
        ordering = ['order']
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['inventory_item']),
        ]

    def __str__(self):
        return f"{self.inventory_item} x {self.quantity}{self.inventory_price.get_unit_display()}"


class OrderShipment(BaseModel):
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
        verbose_name=_("Tracking Number"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Tracking number provided by the carrier."),
    )
    carrier = models.CharField(
        verbose_name=_("Carrier"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Shipping carrier or provider name."),
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=50,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        db_index=True,
    )
    shipped_at = models.DateTimeField(
        verbose_name=_("Shipped At"),
        blank=True,
        null=True,
        db_index=True,
    )
    delivered_at = models.DateTimeField(
        verbose_name=_("Delivered At"),
        blank=True,
        null=True,
        db_index=True,
    )
    notes = models.TextField(
        verbose_name=_("Notes"),
        blank=True,
        null=True,
        help_text=_("Optional notes or instructions for the shipment."),
    )

    class Meta:
        verbose_name = _('Order Shipment')
        verbose_name_plural = _('Order Shipments')
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['status']),
            models.Index(fields=['carrier']),
            models.Index(fields=['shipped_at']),
            models.Index(fields=['delivered_at']),
        ]
        ordering = ['-shipped_at', '-delivered_at']

    def __str__(self):
        return f"Shipment for Order #{self.order.id} ({self.get_status_display()})"

    @property
    def is_shipped(self) -> bool:
        return self.status in [self.StatusChoices.IN_TRANSIT, self.StatusChoices.DELIVERED]

    @property
    def is_delivered(self) -> bool:
        return self.status == self.StatusChoices.DELIVERED

    def mark_shipped(self, tracking_number: str = None, carrier: str = None, notes: str = None):
        self.status = self.StatusChoices.IN_TRANSIT
        self.shipped_at = timezone.now()
        if tracking_number:
            self.tracking_number = tracking_number
        if carrier:
            self.carrier = carrier
        if notes:
            self.notes = notes
        self.save(update_fields=['status', 'shipped_at', 'tracking_number', 'carrier', 'notes'])

    def mark_delivered(self, notes: str = None):
        self.status = self.StatusChoices.DELIVERED
        self.delivered_at = timezone.now()
        if notes:
            self.notes = notes
        self.save(update_fields=['status', 'delivered_at', 'notes'])



class OrderPayment(BaseModel):
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')
        REFUNDED = 'REFUNDED', _('Refunded')

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment',
        verbose_name=_('Order'),
    )
    amount = models.DecimalField(
        max_digits=12,
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
        help_text=_('Unique ID returned by payment gateway'),
        db_index=True,
        unique=True,
    )
    paid_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Paid At'),
        help_text=_('Timestamp when payment was confirmed'),
    )

    class Meta:
        verbose_name = _('Order Payment')
        verbose_name_plural = _('Orders Payments')
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.get_status_display()}"

    def mark_completed(self, transaction_id=None):
        self.status = self.StatusChoices.COMPLETED
        if transaction_id:
            self.transaction_id = transaction_id
        self.paid_at = timezone.now()
        self.save(update_fields=['status', 'transaction_id', 'paid_at'])

    def mark_failed(self, transaction_id=None):
        self.status = self.StatusChoices.FAILED
        if transaction_id:
            self.transaction_id = transaction_id
        self.save(update_fields=['status', 'transaction_id'])

    def is_paid(self):
        return self.status == self.StatusChoices.COMPLETED and self.paid_at is not None
