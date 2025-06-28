from django.contrib import admin
from reversion.admin import VersionAdmin
from nested_admin import NestedModelAdmin, NestedStackedInline
from import_export.admin import ExportMixin

from .models import (
    InventoryBase,
    InventoryItem,
    InventoryTransactionLog,
    LowStockAlert,
    Order,
    OrderItem,
    Shipment,
)

from .resources import (
    InventoryBaseResource,
    InventoryItemResource,
    InventoryTransactionLogResource,
    LowStockAlertResource,
    OrderResource,
    OrderItemResource,
    ShipmentResource,
)


@admin.register(InventoryBase)
class InventoryBaseAdmin(ExportMixin, VersionAdmin):
    resource_class = InventoryBaseResource
    list_display = ('name', 'partner', 'country', 'region', 'is_active', 'created_at', 'updated_at')
    list_filter = ('partner', 'country', 'is_active', 'created_at')
    search_fields = ('name', 'partner__name', 'country__name')


@admin.register(InventoryItem)
class InventoryItemAdmin(ExportMixin, VersionAdmin):
    resource_class = InventoryItemResource
    list_display = (
        'herb', 'base', 'quantity_kg', 'price_usd', 'currency',
        'is_available', 'is_active', 'created_at', 'updated_at'
    )
    list_filter = ('is_available', 'currency', 'base__partner', 'is_active')
    search_fields = ('herb__name', 'base__name')


@admin.register(InventoryTransactionLog)
class InventoryTransactionLogAdmin(ExportMixin, VersionAdmin):
    resource_class = InventoryTransactionLogResource
    list_display = ('inventory_item', 'action', 'quantity_kg', 'performed_by', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('inventory_item__herb__name', 'performed_by__username', 'note')


@admin.register(LowStockAlert)
class LowStockAlertAdmin(ExportMixin, VersionAdmin):
    resource_class = LowStockAlertResource
    list_display = ('inventory_item', 'triggered_at', 'notified')
    list_filter = ('notified',)
    search_fields = ('inventory_item__herb__name', 'inventory_item__base__name')


class OrderItemInline(NestedStackedInline):
    model = OrderItem
    extra = 0
    fields = ('inventory_item', 'quantity_kg', 'unit_price', 'total_price')
    readonly_fields = ('total_price',)


class ShipmentInline(NestedStackedInline):
    model = Shipment
    extra = 0
    fields = ('tracking_number', 'carrier', 'status', 'shipped_at', 'delivered_at')


@admin.register(Order)
class OrderAdmin(ExportMixin, NestedModelAdmin, VersionAdmin):
    resource_class = OrderResource
    list_display = ('id', 'user', 'status', 'total_price', 'is_active', 'created_at', 'updated_at')
    list_filter = ('status', 'is_active', 'created_at')
    search_fields = ('user__username', 'notes')
    inlines = [OrderItemInline, ShipmentInline]


@admin.register(OrderItem)
class OrderItemAdmin(ExportMixin, VersionAdmin):
    resource_class = OrderItemResource
    list_display = ('order', 'inventory_item', 'quantity_kg', 'unit_price', 'total_price')
    list_filter = ('order__status',)
    search_fields = ('inventory_item__herb__name', 'order__user__username')


@admin.register(Shipment)
class ShipmentAdmin(ExportMixin, VersionAdmin):
    resource_class = ShipmentResource
    list_display = ('order', 'tracking_number', 'carrier', 'status', 'shipped_at', 'delivered_at')
    list_filter = ('status', 'carrier')
    search_fields = ('tracking_number', 'order__user__username')
