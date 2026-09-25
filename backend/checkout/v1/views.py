import stripe
import logging
from decimal import Decimal, ROUND_HALF_UP

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.conf import settings
from drf_spectacular.utils import extend_schema

from account.models import Address
from account.v1.serializers import AddressSerializer
from checkout.models import (
    Currency,
    PaymentMethod,
    ShoppingCart,
    ShoppingCartItem,
    Order,
    OrderItem,
    ExchangeRate,

)
from inventory.models import InventoryPrice
from inventory.v1.serializers import InventoryPriceSerializer

from .serializers import (
    CurrencySerializer,
    ShoppingCartSerializer,
    PaymentMethodSerializer,
    OrderSerializer,
)

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

@extend_schema(tags=["Checkout"])
class CurrencyListView(ListAPIView):
    queryset = Currency.objects.filter(is_active=True)
    serializer_class = CurrencySerializer
    permission_classes = [AllowAny]
    pagination_class = None

@extend_schema(tags=["Checkout"])
class PaymentMethodListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer
    pagination_class = None

@extend_schema(tags=["Checkout"])
class ShoppingCartPriceUpdateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        ids_param = request.query_params.get("ids")
        if not ids_param:
            return Response(
                {"error": "Missing 'ids' query parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            ids = [int(pk) for pk in ids_param.split(",") if
                   pk.strip().isdigit()]
        except ValueError:
            return Response(
                {"error": "Invalid 'ids' parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not ids:
            return Response([], status=status.HTTP_200_OK)

        prices = InventoryPrice.objects.filter(id__in=ids).select_related(
            "currency"
        )
        if not prices.exists():
            return Response([], status=status.HTTP_200_OK)

        serializer = InventoryPriceSerializer(
            prices,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Checkout"])
class ShoppingCartView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShoppingCartSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        user = request.user

        shopping_cart, _ = ShoppingCart.objects.get_or_create(user=user)

        serializer = self.serializer_class(
            shopping_cart,
            context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs) -> Response:
        user = request.user
        items: list = request.data

        if not items:
            return Response(
                {"detail": "No items provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        shopping_cart, _ = ShoppingCart.objects.get_or_create(user=user)

        for item in items:
            try:
                price_id = item["price"]["id"]
                quantity = float(item["quantity"])
                if quantity <= 0:
                    return Response(
                        {"detail": "Quantity must be positive."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                price = InventoryPrice.objects.get(id=price_id)

                ShoppingCartItem.objects.update_or_create(
                    cart=shopping_cart,
                    inventory_item=price.inventory_item,
                    inventory_price=price,
                    defaults={"quantity": quantity}
                )

            except KeyError:
                return Response(
                    {"detail": "Invalid item format."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except InventoryPrice.DoesNotExist:
                return Response(
                    {"detail": f"Price ID {price_id} not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            {
                "message": "Your shopping cart has been updated successfully."},
            status=status.HTTP_200_OK
        )

    def delete(self, request: Request, *args, **kwargs) -> Response:
        user = request.user
        item = request.data

        if not item:
            return Response(
                {"detail": "No item provided for deletion."},
                status=status.HTTP_400_BAD_REQUEST
            )

        shopping_cart, _ = ShoppingCart.objects.get_or_create(user=user)

        try:
            price_id = item.get("price_id")

            if price_id is None:
                return Response(
                    {"detail": "Price ID is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                price = InventoryPrice.objects.get(id=price_id)
            except InventoryPrice.DoesNotExist:
                return Response(
                    {"detail": f"Price ID {price_id} not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            deleted, _ = ShoppingCartItem.objects.filter(
                cart=shopping_cart,
                inventory_item=price.inventory_item,
                inventory_price=price
            ).delete()

            return Response(
                {
                    "message": f"Deleted item from your shopping cart."},
                status=status.HTTP_200_OK
            )


        except Exception as e:
            return Response(
                {
                    "detail": f"Error processing item with price ID {price_id}: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

@extend_schema(tags=["Checkout"])
class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()

        address_id = data.get("address_id", None)
        currency_code = data.get("currency_code", "").upper()
        address = None

        # Validate or create address
        if not address_id:
            address_data = data.get("address", {})
            address_data["user"] = user.id
            address_serializer = AddressSerializer(data=address_data)
            if not address_serializer.is_valid():
                return Response(
                    address_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            is_default = address_serializer.data["is_default"]
            if is_default:
                Address.objects.filter(user=user, is_default=True).update(
                    is_default=False
                )
            address = address_serializer.save()
        else:
            address = get_object_or_404(Address, id=address_id, user=user)

        # Get user's active shopping cart and check for items
        try:
            shopping_cart = ShoppingCart.objects.get(user=user)
        except ShoppingCart.DoesNotExist:
            return Response(
                {"detail": "Shopping cart not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_items = shopping_cart.items.filter(is_active=True)
        if not cart_items.exists():
            return Response(
                {"detail": "Shopping cart is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get base currency dynamically
        try:
            base_currency = Currency.objects.get(
                is_base_currency=True,
                is_active=True,
            )
        except Currency.DoesNotExist:
            return Response(
                {"detail": "Base currency not configured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Validate requested currency or fallback to base currency
        if currency_code:
            try:
                currency = Currency.objects.get(
                    code=currency_code,
                    is_active=True
                )
            except Currency.DoesNotExist:
                return Response(
                    {
                        "detail": f"Currency '{currency_code}' not supported."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            currency = base_currency

        # Determine exchange rate (base -> requested)
        if currency == base_currency:
            exchange_rate = Decimal("1")
        else:
            try:
                rate_obj = ExchangeRate.objects.get(
                    base_currency=base_currency,
                    target_currency=currency
                )
                exchange_rate = rate_obj.rate
            except ExchangeRate.DoesNotExist:
                return Response(
                    {
                        "detail": f"No exchange rate from {base_currency.code} to {currency.code}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        total_price = Decimal("0")
        order_items = []

        for item in cart_items:
            base_price = item.inventory_price.price  # assumed in base currency
            quantity = Decimal(str(item.quantity))

            converted_price = (base_price * exchange_rate).quantize(
                Decimal('0.0001'),
                rounding=ROUND_HALF_UP
            )
            item_total = (converted_price * quantity).quantize(
                Decimal('0.0001'),
                rounding=ROUND_HALF_UP
            )
            total_price += item_total

            order_items.append(
                OrderItem(
                    order=None,  # assign later
                    inventory_item=item.inventory_item,
                    inventory_price=item.inventory_price,
                    quantity=quantity,
                    unit_price=converted_price,
                    total_price=item_total,
                )
            )

        order = Order.objects.create(
            user=user,
            delivery_address=address,
            currency=currency,
            status=Order.StatusChoices.PAYMENT,
            total_price=Decimal("0"),
        )

        for oi in order_items:
            oi.order = order
        OrderItem.objects.bulk_create(order_items)

        order.total_price = total_price.quantize(
            Decimal('0.0001'),
            rounding=ROUND_HALF_UP
        )
        order.save(update_fields=["total_price"])

        cart_items.delete()

        return Response(
            {"order_id": order.id},
            status=status.HTTP_201_CREATED
        )

@extend_schema(tags=["Checkout"])
class UserOrderView(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user)
        return queryset

@extend_schema(tags=["Checkout"])
class StripePaymentOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        order_id = request.data.get("order_id")

        if not order_id:
            return Response(
                {"detail": "Order ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch the order and validate
        order = get_object_or_404(Order, id=order_id, user=user)

        if order.status != Order.StatusChoices.PAYMENT:
            return Response(
                {"detail": "Order is not in a payable state."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Stripe expects amount in cents as integer
        try:
            amount_cents = int(order.total_price * 100)
        except Exception:
            return Response(
                {"detail": "Invalid order total price."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': order.currency.code.lower(),
                            'product_data': {
                                'name': f"Order #{order.id}",
                                'description': f"Payment for order #{order.id} at terrapura",
                            },
                            'unit_amount': amount_cents,
                        },
                        'quantity': 1,
                    },
                ],
                customer_email=order.user.email,
                mode='payment',
                success_url=f"{settings.FRONTEND_DOMAIN}/checkout/payment-result?success=true&order_id={order.id}&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.FRONTEND_DOMAIN}/checkout/payment-result?success=false&order_id={order.id}",
                metadata={
                    "order_id": str(order.id),
                    "user_id": str(user.id),
                },
            )
        except Exception as e:
            return Response(
                {"detail": f"Stripe error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"checkout_url": session.url})
