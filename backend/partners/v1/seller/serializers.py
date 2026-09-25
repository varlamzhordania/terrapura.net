from rest_framework import serializers

from inventory.models import InventoryBase, InventoryItem
from inventory.v1.serializers import InventoryItemShortSerializer


class InventoryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryBase
        fields = '__all__'


class InventoryItemListSerializer(InventoryItemShortSerializer):
    class Meta:
        model = InventoryItem
        fields = [
            'id', 'herb', 'base', 'unit', 'quantity', 'expiration_date',
            'is_available', 'low_stock_threshold'
        ]


class InventoryItemCreateEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = [
            'id', 'herb', 'base', 'quantity','quantity_unit', 'expiration_date',
            'is_available', 'low_stock_threshold'
        ]
