from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from core.mixins import OptionalPaginationMixin

from partners.models import Partner


class PartnerScopedViewSet(OptionalPaginationMixin, ModelViewSet):
    """
    Base ViewSet for seller dashboard CRUD endpoints.
    Ensures that the partner exists and that the user belongs to it.
    Automatically filters queryset by partner_id from the URL.
    """
    permission_classes = [IsAuthenticated]
    partner_lookup_url_kwarg = "partner_id"
    partner_lookup_field = "partner"

    def get_partner(self):
        partner_id = self.kwargs.get(self.partner_lookup_url_kwarg)
        try:
            partner = Partner.objects.get(id=partner_id)
        except Partner.DoesNotExist:
            raise PermissionDenied("Invalid partner id.")

        # check membership
        if not partner.staff_members.filter(
                user_id=self.request.user.id
        ).exists():
            raise PermissionDenied(
                "you do not have permission to view this data."
            )

        return partner

    def get_queryset(self):
        qs = super().get_queryset()
        partner = self.get_partner()

        partner_field = getattr(self, "partner_lookup_field", "partner")

        return qs.filter(**{partner_field: partner})

    def perform_create(self, serializer):
        partner = self.get_partner()
        serializer.save(partner=partner)
