from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import extend_schema

from partners.models import Partner
from partners.v1.serializers import PartnerSerializer


@extend_schema(tags=["Partners"])
class PartnerDetailAPIView(RetrieveAPIView):
    queryset = Partner.objects.filter(is_active=True)
    serializer_class = PartnerSerializer
