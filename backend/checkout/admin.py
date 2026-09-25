from django.contrib import admin
from import_export.admin import ExportMixin
from reversion.admin import VersionAdmin
from nested_admin import (
    NestedModelAdmin, NestedTabularInline,
    NestedStackedInline,
)

from .models import (
    Currency,
    ExchangeRate,
    PaymentMethod,
    ShoppingCart,
    ShoppingCartItem,
    OrderPayment,
    Order,
    OrderItem,
    OrderShipment,
)
from .resources import (
    CurrencyResource,
    ExchangeRateResource,
    ShoppingCartResource,
    ShoppingCartItemResource,
    PaymentResource,
    OrderResource,
    OrderItemResource,
    OrderShipmentResource,
    PaymentMethodResource,
)


class ShoppingCartItemInline(NestedTabularInline):
    model = ShoppingCartItem
    extra = 0
    fields = ('inventory_item', 'inventory_price', 'quantity')


@admin.register(Currency)
class CurrencyAdmin(ExportMixin, VersionAdmin):
    resource_class = CurrencyResource
    list_display = (
        'code', 'name', 'symbol', 'is_base_currency', 'is_active',
        'created_at',
        'updated_at')
    list_filter = (
        'is_base_currency', 'is_active', 'created_at', 'updated_at')
    search_fields = ('code', 'name', 'symbol')
    ordering = ('code',)


@admin.register(ExchangeRate)
class ExchangeRateAdmin(ExportMixin, VersionAdmin):
    resource_class = ExchangeRateResource
    list_display = (
        'base_currency', 'target_currency', 'rate', 'created_at',
        'updated_at')
    search_fields = ('base_currency__code', 'target_currency__code')
    ordering = ('base_currency', 'target_currency')


@admin.register(PaymentMethod)
class PaymentMethodAdmin(ExportMixin, VersionAdmin):
    resource_class = PaymentMethodResource
    list_display = (
        'name', 'code', 'min_amount',
        'min_currency', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(ExportMixin, NestedModelAdmin, VersionAdmin):
    resource_class = ShoppingCartResource
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__email',)
    ordering = ('-created_at',)
    inlines = (ShoppingCartItemInline,)


@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(ExportMixin, VersionAdmin):
    resource_class = ShoppingCartItemResource
    list_display = (
        'cart', 'inventory_item', 'inventory_price', 'quantity',
        'created_at',
        'updated_at')
    search_fields = ('inventory_item__herb__name',)
    ordering = ('-created_at',)


@admin.register(OrderPayment)
class PaymentAdmin(ExportMixin, VersionAdmin):
    resource_class = PaymentResource
    list_display = (
        'order', 'amount', 'currency', 'status', 'method', 'paid_at',
        'created_at')
    search_fields = ('order__id', 'transaction_id', 'method')
    list_filter = ('status', 'method', 'currency')
    ordering = ('-created_at',)


class OrderPaymentInline(NestedStackedInline):
    model = OrderPayment
    extra = 0
    fields = (
        "order",
        "amount",
        "currency",
        "status",
        "method",
        "transaction_id",
        "paid_at",
        "created_at",
        "updated_at"
    )
    readonly_fields = (
        'amount', 'transaction_id', 'paid_at', 'created_at',
        'updated_at')


class OrderItemInline(NestedStackedInline):
    model = OrderItem
    extra = 0
    fields = (
        'inventory_item', 'inventory_price', 'quantity', 'unit_price',
        'total_price')
    readonly_fields = ('total_price',)


class OrderShipmentInline(NestedStackedInline):
    model = OrderShipment
    extra = 0
    fields = (
        'tracking_number', 'carrier', 'status', 'shipped_at',
        'delivered_at')


@admin.register(Order)
class OrderAdmin(ExportMixin, NestedModelAdmin, VersionAdmin):
    resource_class = OrderResource
    list_display = (
        'id', 'user', 'status', 'total_price', 'currency', 'is_active',
        'created_at',
        'updated_at')
    list_filter = ('status', 'is_active', 'created_at')
    search_fields = ('user__email', 'notes')
    inlines = [OrderPaymentInline, OrderShipmentInline, OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(ExportMixin, VersionAdmin):
    resource_class = OrderItemResource
    list_display = (
        'order', 'inventory_item', 'inventory_price', 'quantity',
        'unit_price', 'total_price')
    list_filter = ('order__status',)
    search_fields = ('inventory_item__herb__name', 'order__user__email')


@admin.register(OrderShipment)
class OrderShipmentAdmin(ExportMixin, VersionAdmin):
    resource_class = OrderShipmentResource
    list_display = (
        'order', 'tracking_number', 'carrier', 'status', 'shipped_at',
        'delivered_at')
    list_filter = ('status', 'carrier')
    search_fields = ('tracking_number', 'order__user__email')
