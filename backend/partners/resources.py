from import_export import resources

from .models import (
    Region,
    Country,
    Partner,
    PartnerContact,
    PartnerStaff,
    PartnerReview,
    PartnerWallet,
    WalletTransaction,
)


class RegionResource(resources.ModelResource):
    class Meta:
        model = Region


class CountryResource(resources.ModelResource):
    class Meta:
        model = Country


class PartnerResource(resources.ModelResource):
    class Meta:
        model = Partner


class PartnerContactResource(resources.ModelResource):
    class Meta:
        model = PartnerContact


class PartnerStaffResource(resources.ModelResource):
    class Meta:
        model = PartnerStaff


class PartnerReviewResource(resources.ModelResource):
    class Meta:
        model = PartnerReview


class PartnerWalletResource(resources.ModelResource):
    class Meta:
        model = PartnerWallet


class WalletTransactionResource(resources.ModelResource):
    class Meta:
        model = WalletTransaction
