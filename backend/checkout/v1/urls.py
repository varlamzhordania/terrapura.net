from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    CurrencyListView,
    PaymentMethodListView,
    ShoppingCartPriceUpdateView,
    ShoppingCartView,
    OrderCreateAPIView,
    UserOrderView,
    StripePaymentOrderAPIView,
)
from .webhooks import stripe_webhook_view

router = SimpleRouter()
router.register('orders', UserOrderView, basename='order')

app_name = 'checkout-v1'
urlpatterns = [
    path('currencies/', CurrencyListView.as_view(), name='currencies'),
    path(
        'payment-methods/',
        PaymentMethodListView.as_view(),
        name='payment_methods'
    ),
    path(
        'cart/prices/',
        ShoppingCartPriceUpdateView.as_view(),
        name='shopping_cart_prices_update'
    ),
    path(
        'cart/',
        ShoppingCartView.as_view(),
        name='shopping_cart'
    ),
    path(
        'orders/create/',
        OrderCreateAPIView.as_view(),
        name='order_create'
    ),
    path('stripe/', StripePaymentOrderAPIView.as_view(), name='stripe'),

]

urlpatterns += router.urls

urlpatterns += [
    path('stripe/webhook/', stripe_webhook_view, name='stripe_webhook'),
]
