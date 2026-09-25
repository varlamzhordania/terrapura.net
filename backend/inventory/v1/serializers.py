from decimal import Decimal, ROUND_HALF_UP
from rest_framework import serializers
from inventory.models import InventoryBase, InventoryItem, InventoryPrice

from checkout.v1.serializers import CurrencySerializer
from checkout.models import Currency, ExchangeRate
from herbs.v1.serializers import HerbShortSerializer


class InventoryBaseSerializer(serializers.ModelSerializer):
    partner = serializers.CharField(source='partner.name', read_only=True)
    country = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = InventoryBase
        fields = ['id', 'partner', 'name', 'country', 'region', 'address',
                  'contact_person', ]


class InventoryPriceSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(many=False, read_only=True)
    converted_price = serializers.SerializerMethodField()
    converted_currency = serializers.SerializerMethodField()

    class Meta:
        model = InventoryPrice
        fields = [
            'id', 'unit', 'price', 'currency',
            'converted_price', 'converted_currency'
        ]

    def _quantize_for_display(self, value: Decimal):
        """Show 4 decimals normally, but keep up to 6 for very small values."""
        if value == 0:
            return "0"

        # Try 4 decimal places first
        q2 = value.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
        if q2 != 0:
            return str(q2.normalize())
        # If 2 decimals gives 0 but value > 0, show 6 decimals
        q6 = value.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
        return str(q6.normalize())

    def get_converted_price(self, obj):
        request = self.context.get('request')
        if not request:
            return None

        target_currency_code = request.query_params.get('currency')
        if not target_currency_code:
            return None

        target_currency_code = target_currency_code.upper()
        try:
            target_currency = Currency.objects.get(
                code=target_currency_code
            )
        except Currency.DoesNotExist:
            return None

        if obj.currency == target_currency:
            return str(self._quantize_for_display(Decimal(obj.price)))

        # Try direct conversion
        try:
            rate_obj = ExchangeRate.objects.get(
                base_currency=obj.currency,
                target_currency=target_currency
            )
            converted = Decimal(obj.price) * Decimal(rate_obj.rate)
            return self._quantize_for_display(converted)
        except ExchangeRate.DoesNotExist:
            # Try inverse rate
            try:
                inverse_rate = ExchangeRate.objects.get(
                    base_currency=target_currency,
                    target_currency=obj.currency
                )
                converted = Decimal(obj.price) / Decimal(inverse_rate.rate)
                return self._quantize_for_display(converted)
            except ExchangeRate.DoesNotExist:
                return None

    def get_converted_currency(self, obj):
        request = self.context.get('request')
        if not request:
            return None

        target_currency_code = request.query_params.get('currency')
        return target_currency_code.upper() if target_currency_code else None


class InventoryItemShortSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(source='get_quantity_unit_display')
    country = serializers.CharField(source='base.country.name')
    herb = HerbShortSerializer(many=False, read_only=True)
    base = InventoryBaseSerializer(many=False, read_only=True)

    class Meta:
        model = InventoryItem
        fields = [
            'id', 'herb', 'country', 'base', 'unit'
        ]


class InventoryOfferSerializer(serializers.ModelSerializer):
    base = InventoryBaseSerializer(many=False, read_only=True)
    country = serializers.CharField(source='base.country.name')
    quantity = serializers.FloatField()
    unit = serializers.CharField(source='get_quantity_unit_display')
    prices = InventoryPriceSerializer(many=True, read_only=True)

    class Meta:
        model = InventoryItem
        fields = ['id', 'base', 'country', 'quantity', 'unit',
                  'is_available', 'prices']
