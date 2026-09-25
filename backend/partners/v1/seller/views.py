from partners.viewsets import PartnerScopedViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema

from inventory.models import InventoryBase, InventoryItem

from partners.v1.seller.serializers import (
    InventoryBaseSerializer,
    InventoryItemListSerializer,
    InventoryItemCreateEditSerializer,
)


@extend_schema(tags=["Partners"])
class InventoryBaseViewSet(PartnerScopedViewSet):
    permission_classes = [IsAuthenticated]
    queryset = InventoryBase.objects.all()
    serializer_class = InventoryBaseSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


@extend_schema(tags=["Partners"])
class InventoryItemViewSet(PartnerScopedViewSet):
    permission_classes = [IsAuthenticated]
    queryset = InventoryItem.objects.all()
    partner_lookup_field = "base__partner"
    filter_backends = [SearchFilter]
    search_fields = ['herb__name', ]

    def get_serializer_class(self):
        if self.action == "list":
            return InventoryItemListSerializer
        if self.action == "retrieve":
            return InventoryItemListSerializer
        return InventoryItemCreateEditSerializer
