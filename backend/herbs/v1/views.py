from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch

from core.mixins import OptionalPaginationMixin
from herbs.models import (
    Herb,
    Category,
    Tag,
)

from inventory.models import (
    InventoryItem,
    InventoryPrice,
)
from inventory.v1.serializers import (
    InventoryOfferSerializer,
)

from .serializers import (
    HerbSerializer,
    HerbSEOSerializer,
    CategorySerializer,
    TagSerializer,
    Symptom,
    SymptomSerializer,
)
from .filters import HerbFilter


class HerbsList(OptionalPaginationMixin, ListAPIView):
    permission_classes = [AllowAny]
    queryset = Herb.objects.filter(is_active=True)
    serializer_class = HerbSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = HerbFilter
    search_fields = ['name', 'latin_name', 'description']
    ordering_fields = ['name', 'created_at']


class HerbDetail(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Herb.objects.filter(is_active=True)
    serializer_class = HerbSEOSerializer
    lookup_field = "slug"


class HerbOffer(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request, slug: str, *args, **kwargs) -> Response:
        try:
            herb = Herb.objects.get(slug=slug, is_active=True)
        except Herb.DoesNotExist:
            return Response({"detail": "Herb not found."}, status=status.HTTP_404_NOT_FOUND)

        inventory_items = (
            InventoryItem.objects.filter(herb=herb, is_available=True)
            .select_related('base__partner')
            .prefetch_related(
                Prefetch('prices', queryset=InventoryPrice.objects.select_related('currency'))
            )
        )

        offers = InventoryOfferSerializer(inventory_items, many=True).data
        return Response(offers, status=status.HTTP_200_OK)


class CategoryList(OptionalPaginationMixin, ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class TagList(OptionalPaginationMixin, ListAPIView):
    permission_classes = [AllowAny]
    queryset = Tag.objects.filter(is_active=True)
    serializer_class = TagSerializer


class SymptomList(OptionalPaginationMixin, ListAPIView):
    permission_classes = [AllowAny]
    queryset = Symptom.objects.filter(is_active=True)
    serializer_class = SymptomSerializer
