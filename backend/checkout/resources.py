from import_export import resources
from .models import (
    Currency,
    ExchangeRate,
    ShoppingCart,
    ShoppingCartItem,
    Payment,
)

class CurrencyResource(resources.ModelResource):
    class Meta:
        model = Currency


class ExchangeRateResource(resources.ModelResource):
    class Meta:
        model = ExchangeRate


class ShoppingCartResource(resources.ModelResource):
    class Meta:
        model = ShoppingCart


class ShoppingCartItemResource(resources.ModelResource):
    class Meta:
        model = ShoppingCartItem


class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment
