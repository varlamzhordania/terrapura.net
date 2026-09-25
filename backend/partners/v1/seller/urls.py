from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import InventoryBaseViewSet, InventoryItemViewSet

router = SimpleRouter()

router.register(
    r'^(?P<partner_id>\d+)/inventory/base',
    InventoryBaseViewSet
)
router.register(
    r'^(?P<partner_id>\d+)/inventory/product',
    InventoryItemViewSet
)

urlpatterns = []

urlpatterns += router.urls
