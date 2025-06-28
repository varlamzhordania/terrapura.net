from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DecimalWidget
from django.contrib.auth import get_user_model

from .models import (
    InventoryBase,
    InventoryItem,
    InventoryTransactionLog,
    LowStockAlert,
    Order,
    OrderItem,
    Shipment
)

User = get_user_model()


class InventoryBaseResource(resources.ModelResource):
    partner = fields.Field(
        column_name='partner',
        attribute='partner',
        widget=ForeignKeyWidget('partners.Partner', 'name')
    )
    country = fields.Field(
        column_name='country',
        attribute='country',
        widget=ForeignKeyWidget('partners.Country', 'name')
    )

    class Meta:
        model = InventoryBase
        fields = ('id', 'partner', 'name', 'country', 'region', 'address', 'contact_person', 'created_at', 'updated_at')
        export_order = fields


class InventoryItemResource(resources.ModelResource):
    herb = fields.Field(
        column_name='herb',
        attribute='herb',
        widget=ForeignKeyWidget('herbs.Herb', 'name')
    )
    base = fields.Field(
        column_name='inventory_base',
        attribute='base',
        widget=ForeignKeyWidget(InventoryBase, 'name')
    )

    class Meta:
        model = InventoryItem
        fields = (
            'id', 'herb', 'base', 'quantity_kg', 'price_usd', 'currency',
            'expiration_date', 'low_stock_threshold_kg', 'is_available',
            'created_at', 'updated_at'
        )
        export_order = fields


class InventoryTransactionLogResource(resources.ModelResource):
    inventory_item = fields.Field(
        column_name='inventory_item',
        attribute='inventory_item',
        widget=ForeignKeyWidget(InventoryItem, '__str__')
    )
    performed_by = fields.Field(
        column_name='performed_by',
        attribute='performed_by',
        widget=ForeignKeyWidget(User, 'username')
    )

    class Meta:
        model = InventoryTransactionLog
        fields = (
            'id', 'inventory_item', 'action', 'quantity_kg',
            'performed_by', 'note', 'created_at', 'updated_at'
        )
        export_order = fields


class LowStockAlertResource(resources.ModelResource):
    inventory_item = fields.Field(
        column_name='inventory_item',
        attribute='inventory_item',
        widget=ForeignKeyWidget(InventoryItem, '__str__')
    )

    class Meta:
        model = LowStockAlert
        fields = ('id', 'inventory_item', 'triggered_at', 'notified', 'created_at', 'updated_at')
        export_order = fields


class OrderResource(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'total_price', 'notes', 'created_at', 'updated_at')
        export_order = fields


class OrderItemResource(resources.ModelResource):
    order = fields.Field(
        column_name='order',
        attribute='order',
        widget=ForeignKeyWidget(Order, 'id')
    )
    inventory_item = fields.Field(
        column_name='inventory_item',
        attribute='inventory_item',
        widget=ForeignKeyWidget(InventoryItem, '__str__')
    )

    class Meta:
        model = OrderItem
        fields = (
            'id', 'order', 'inventory_item', 'quantity_kg',
            'unit_price', 'total_price'
        )
        export_order = fields


class ShipmentResource(resources.ModelResource):
    order = fields.Field(
        column_name='order',
        attribute='order',
        widget=ForeignKeyWidget(Order, 'id')
    )

    class Meta:
        model = Shipment
        fields = (
            'id', 'order', 'tracking_number', 'carrier',
            'status', 'shipped_at', 'delivered_at',
            'created_at', 'updated_at'
        )
        export_order = fields
