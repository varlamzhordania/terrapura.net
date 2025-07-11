from rest_framework import serializers
from inventory.models import InventoryBase, InventoryItem, InventoryPrice

from checkout.v1.serializers import CurrencySerializer


class InventoryBaseSerializer(serializers.ModelSerializer):
    partner = serializers.CharField(source='partner.name', read_only=True)
    country = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = InventoryBase
        fields = ['partner', 'name', 'country', 'region', 'address', 'contact_person', ]


class InventoryPriceSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(many=False, read_only=True)

    class Meta:
        model = InventoryPrice
        fields = ['id', 'unit', 'price', 'currency']


class InventoryOfferSerializer(serializers.ModelSerializer):
    base = InventoryBaseSerializer(many=False)
    country = serializers.CharField(source='base.country.name')
    quantity = serializers.FloatField()
    unit = serializers.CharField(source='get_quantity_unit_display')
    prices = InventoryPriceSerializer(many=True)

    class Meta:
        model = InventoryItem
        fields = ['id', 'base', 'country', 'quantity', 'unit', 'is_available', 'prices']
