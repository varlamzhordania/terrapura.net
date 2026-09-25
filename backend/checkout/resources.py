from import_export import resources
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


class CurrencyResource(resources.ModelResource):
    class Meta:
        model = Currency


class ExchangeRateResource(resources.ModelResource):
    class Meta:
        model = ExchangeRate


class PaymentMethodResource(resources.ModelResource):
    class Meta:
        model = PaymentMethod


class ShoppingCartResource(resources.ModelResource):
    class Meta:
        model = ShoppingCart


class ShoppingCartItemResource(resources.ModelResource):
    class Meta:
        model = ShoppingCartItem


class PaymentResource(resources.ModelResource):
    class Meta:
        model = OrderPayment


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order


class OrderItemResource(resources.ModelResource):
    class Meta:
        model = OrderItem


class OrderShipmentResource(resources.ModelResource):
    class Meta:
        model = OrderShipment
