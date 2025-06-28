from django.contrib import admin
from reversion.admin import VersionAdmin
from nested_admin import NestedModelAdmin, NestedStackedInline
from import_export.admin import ExportMixin

from .models import (
    Region,
    Country,
    Partner,
    PartnerContact,
    PartnerStaff,
    PartnerProduct,
    PartnerReview,
)

from .resources import (
    RegionResource,
    CountryResource,
    PartnerResource,
    PartnerContactResource,
    PartnerStaffResource,
    PartnerProductResource,
    PartnerReviewResource,
)


@admin.register(Region)
class RegionAdmin(ExportMixin, VersionAdmin):
    resource_class = RegionResource
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Country)
class CountryAdmin(ExportMixin, VersionAdmin):
    resource_class = CountryResource
    list_display = ('name', 'iso_code', 'region', 'is_active', 'created_at', 'updated_at')
    list_filter = ('region', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'iso_code')


class PartnerContactInline(NestedStackedInline):
    model = PartnerContact
    extra = 1
    fields = ('name', 'type', 'value', 'is_active')
    ordering = ('type',)


class PartnerStaffInline(NestedStackedInline):
    model = PartnerStaff
    extra = 1
    fields = ('user', 'role', 'is_active')
    ordering = ('role',)


class PartnerProductInline(NestedStackedInline):
    model = PartnerProduct
    extra = 1
    fields = ('herb', 'is_available', 'is_active')
    ordering = ('herb',)


@admin.register(Partner)
class PartnerAdmin(ExportMixin, NestedModelAdmin, VersionAdmin):
    resource_class = PartnerResource
    list_display = ('name', 'country', 'verified', 'rating', 'is_active', 'created_at', 'updated_at')
    list_filter = ('verified', 'country', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    inlines = [PartnerContactInline, PartnerStaffInline, PartnerProductInline]


@admin.register(PartnerContact)
class PartnerContactAdmin(ExportMixin, VersionAdmin):
    resource_class = PartnerContactResource
    list_display = ('partner', 'name', 'type', 'value', 'is_active', 'created_at', 'updated_at')
    list_filter = ('type', 'is_active', 'created_at', 'updated_at')
    search_fields = ('partner__name', 'name', 'value')


@admin.register(PartnerStaff)
class PartnerStaffAdmin(ExportMixin, VersionAdmin):
    resource_class = PartnerStaffResource
    list_display = ('partner', 'user', 'role', 'is_active', 'created_at', 'updated_at')
    list_filter = ('role', 'is_active', 'created_at', 'updated_at')
    search_fields = ('partner__name', 'user__username')


@admin.register(PartnerProduct)
class PartnerProductAdmin(ExportMixin, VersionAdmin):
    resource_class = PartnerProductResource
    list_display = ('partner', 'herb', 'is_available', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_available', 'is_active', 'created_at', 'updated_at')
    search_fields = ('partner__name', 'herb__name')


@admin.register(PartnerReview)
class PartnerReviewAdmin(ExportMixin, VersionAdmin):
    resource_class = PartnerReviewResource
    list_display = ('partner', 'user', 'rating', 'approved', 'is_active', 'created_at', 'updated_at')
    list_filter = ('approved', 'rating', 'is_active', 'created_at', 'updated_at')
    search_fields = ('partner__name', 'user__username', 'comment')
