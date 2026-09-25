from decimal import Decimal, ROUND_HALF_UP
from rest_framework import serializers

from checkout.models import (
    Currency,
    ExchangeRate,
    PaymentMethod,
    ShoppingCart,
    ShoppingCartItem,
    Order,
    OrderItem,
    OrderPayment,
    OrderShipment,
)

from account.v1.serializers import ListAddressSerializer
from herbs.v1.serializers import HerbShortSerializer


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['code', 'name', 'symbol']


class PaymentMethodSerializer(serializers.ModelSerializer):
    converted_min_amount = serializers.SerializerMethodField()
    converted_currency = serializers.SerializerMethodField()

    class Meta:
        model = PaymentMethod
        fields = [
            'code', 'name', 'description', 'icon',
            'min_amount', 'min_currency',
            'converted_min_amount', 'converted_currency'
        ]

    def _quantize_for_display(self, value: Decimal):
        """Show 2 decimals normally, but keep up to 6 for very small values."""
        if value == 0:
            return "0"

        q2 = value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if q2 != 0:
            return str(q2.normalize())

        q6 = value.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
        return str(q6.normalize())

    def get_converted_min_amount(self, obj):
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

        if obj.min_currency == target_currency:
            return self._quantize_for_display(Decimal(obj.min_amount))

        # Try direct rate
        try:
            rate_obj = ExchangeRate.objects.get(
                base_currency__code=obj.min_currency,
                target_currency=target_currency
            )
            converted = Decimal(obj.min_amount) * Decimal(rate_obj.rate)
            return self._quantize_for_display(converted)
        except ExchangeRate.DoesNotExist:
            # Try inverse rate
            try:
                inverse_rate = ExchangeRate.objects.get(
                    base_currency=target_currency,
                    target_currency=obj.min_currency
                )
                converted = Decimal(obj.min_amount) / Decimal(
                    inverse_rate.rate
                )
                return self._quantize_for_display(converted)
            except ExchangeRate.DoesNotExist:
                return None

    def get_converted_currency(self, obj):
        request = self.context.get('request')
        if not request:
            return None

        target_currency_code = request.query_params.get('currency')
        return target_currency_code.upper() if target_currency_code else None


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    herb = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCartItem
        fields = ['herb', 'price', 'quantity']

    def get_herb(self, obj):
        herb = obj.inventory_item.herb
        serializer = HerbShortSerializer(
            herb,
            many=False,
            context={'request': self.context.get('request')}
        )
        return serializer.data

    def get_price(self, obj):
        from inventory.v1.serializers import InventoryPriceSerializer

        price = obj.inventory_price
        serializer = InventoryPriceSerializer(
            price,
            many=False,
            context={'request': self.context.get('request')}
        )
        return serializer.data


class ShoppingCartSerializer(serializers.ModelSerializer):
    items = ShoppingCartItemSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = ['items']


class OrderPaymentPublicSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(many=False, read_only=True)

    class Meta:
        model = OrderPayment
        fields = [
            'amount',
            'currency',
            'status',
            'method',
            'transaction_id',
            'paid_at',
            'created_at',
            'updated_at',
        ]


class OrderShipmentPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderShipment
        fields = [
            'tracking_number',
            'carrier',
            'status',
            'shipped_at',
            'delivered_at',
            'notes',
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    inventory_item = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "inventory_item",
            "inventory_price",
            "quantity",
            "unit_price",
            "total_price",
        ]

    def get_inventory_item(self, obj):
        from inventory.v1.serializers import InventoryItemShortSerializer

        return InventoryItemShortSerializer(obj.inventory_item).data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    delivery_address = ListAddressSerializer(many=False, read_only=True)
    currency = CurrencySerializer(many=False, read_only=True)
    payment = OrderPaymentPublicSerializer(many=False, read_only=True)
    shipment = OrderShipmentPublicSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "delivery_address",
            "status",
            "total_price",
            "currency",
            "notes",
            "is_approved_by_customer",
            "approved_at",
            "escrow_released",
            "released_at",
            "created_at",
            "updated_at",
            "items",
            "shipment",
            "payment",
        ]
