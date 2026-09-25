from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
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


@extend_schema(tags=["Herbs"])
class HerbsListView(OptionalPaginationMixin, ListAPIView):
    permission_classes = [AllowAny]
    queryset = Herb.objects.filter(is_active=True)
    serializer_class = HerbSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = HerbFilter
    search_fields = ['name', 'latin_name', 'description']
    ordering_fields = ['name', 'created_at']


@extend_schema(tags=["Herbs"])
class HerbDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Herb.objects.filter(is_active=True)
    serializer_class = HerbSEOSerializer
    lookup_field = "slug"


@extend_schema(tags=["Herbs"])
class HerbOfferView(APIView):
    permission_classes = [AllowAny]

    def get(
            self,
            request: Request,
            slug: str,
            *args,
            **kwargs
            ) -> Response:
        herb = get_object_or_404(Herb, slug=slug, is_active=True)

        inventory_items = (
            InventoryItem.objects.filter(herb=herb, is_available=True)
            .select_related('base__partner')
            .prefetch_related(
                Prefetch(
                    'prices',
                    queryset=InventoryPrice.objects.select_related(
                        'currency'
                        )
                    )
            )
        )

        serializer = InventoryOfferSerializer(
            inventory_items,
            many=True,
            context={'request': request}
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Herbs"])
class CategoryListView(OptionalPaginationMixin, ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


@extend_schema(tags=["Herbs"])
class TagListView(OptionalPaginationMixin, ListAPIView):
    permission_classes = [AllowAny]
    queryset = Tag.objects.filter(is_active=True)
    serializer_class = TagSerializer


@extend_schema(tags=["Herbs"])
class SymptomListView(OptionalPaginationMixin, ListAPIView):
    permission_classes = [AllowAny]
    queryset = Symptom.objects.filter(is_active=True)
    serializer_class = SymptomSerializer
