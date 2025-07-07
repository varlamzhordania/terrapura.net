from import_export import resources
from django.contrib.auth import get_user_model

from .models import (
    InventoryBase,
    InventoryItem,
    InventoryPrice,
    InventoryTransactionLog,
    LowStockAlert,
    Order,
    OrderItem,
    Shipment,
)

User = get_user_model()


class InventoryBaseResource(resources.ModelResource):
    class Meta:
        model = InventoryBase


class InventoryItemResource(resources.ModelResource):
    class Meta:
        model = InventoryItem


class InventoryPriceResource(resources.ModelResource):
    class Meta:
        model = InventoryPrice


class InventoryTransactionLogResource(resources.ModelResource):
    class Meta:
        model = InventoryTransactionLog


class LowStockAlertResource(resources.ModelResource):
    class Meta:
        model = LowStockAlert


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order


class OrderItemResource(resources.ModelResource):
    class Meta:
        model = OrderItem


class ShipmentResource(resources.ModelResource):
    class Meta:
        model = Shipment
