from django.contrib import admin
from import_export.admin import ExportMixin
from reversion.admin import VersionAdmin
from nested_admin import NestedModelAdmin, NestedTabularInline

from .models import (
    Currency,
    ExchangeRate,
    ShoppingCart,
    ShoppingCartItem,
    Payment,
)
from .resources import (
    CurrencyResource,
    ExchangeRateResource,
    ShoppingCartResource,
    ShoppingCartItemResource,
    PaymentResource,
)


class ShoppingCartItemInline(NestedTabularInline):
    model = ShoppingCartItem
    extra = 0


@admin.register(Currency)
class CurrencyAdmin(ExportMixin, VersionAdmin):
    resource_class = CurrencyResource
    list_display = ('code', 'name', 'symbol', 'created_at', 'updated_at')
    search_fields = ('code', 'name', 'symbol')
    ordering = ('code',)


@admin.register(ExchangeRate)
class ExchangeRateAdmin(ExportMixin, VersionAdmin):
    resource_class = ExchangeRateResource
    list_display = ('base_currency', 'target_currency', 'rate', 'created_at', 'updated_at')
    search_fields = ('base_currency__code', 'target_currency__code')
    ordering = ('base_currency', 'target_currency')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(ExportMixin, NestedModelAdmin, VersionAdmin):
    resource_class = ShoppingCartResource
    list_display = ('user', 'partner', 'created_at', 'updated_at')
    search_fields = ('user__email', 'partner__name')
    ordering = ('-created_at',)
    inlines = (ShoppingCartItemInline,)


@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(ExportMixin, VersionAdmin):
    resource_class = ShoppingCartItemResource
    list_display = ('cart', 'inventory_item', 'quantity_kg', 'created_at', 'updated_at')
    search_fields = ('inventory_item__herb__name',)
    ordering = ('-created_at',)


@admin.register(Payment)
class PaymentAdmin(ExportMixin, VersionAdmin):
    resource_class = PaymentResource
    list_display = ('order', 'amount', 'currency', 'status', 'method', 'paid_at', 'created_at')
    search_fields = ('order__id', 'transaction_id', 'method')
    list_filter = ('status', 'method', 'currency')
    ordering = ('-created_at',)
