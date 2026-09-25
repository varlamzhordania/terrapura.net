from import_export import resources
from django.contrib.auth import get_user_model

from .models import (
    InventoryBase,
    InventoryItem,
    InventoryPrice,
    InventoryTransactionLog,
    LowStockAlert,
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


