from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth import get_user_model

from .models import (
    Region,
    Country,
    Partner,
    PartnerContact,
    PartnerStaff,
    PartnerProduct,
    PartnerReview
)

User = get_user_model()


class RegionResource(resources.ModelResource):
    class Meta:
        model = Region
        fields = ('id', 'name', 'created_at', 'updated_at')
        export_order = fields


class CountryResource(resources.ModelResource):
    region = fields.Field(
        column_name='region',
        attribute='region',
        widget=ForeignKeyWidget(Region, 'name')
    )

    class Meta:
        model = Country
        fields = ('id', 'name', 'iso_code', 'region', 'created_at', 'updated_at')
        export_order = fields


class PartnerResource(resources.ModelResource):
    country = fields.Field(
        column_name='country',
        attribute='country',
        widget=ForeignKeyWidget(Country, 'name')
    )

    class Meta:
        model = Partner
        fields = (
            'id', 'name', 'country', 'address', 'website', 'description',
            'verified', 'rating', 'created_at', 'updated_at'
        )
        export_order = fields


class PartnerContactResource(resources.ModelResource):
    partner = fields.Field(
        column_name='partner',
        attribute='partner',
        widget=ForeignKeyWidget(Partner, 'name')
    )

    class Meta:
        model = PartnerContact
        fields = ('id', 'partner', 'name', 'type', 'value', 'created_at', 'updated_at')
        export_order = fields


class PartnerStaffResource(resources.ModelResource):
    partner = fields.Field(
        column_name='partner',
        attribute='partner',
        widget=ForeignKeyWidget(Partner, 'name')
    )
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )

    class Meta:
        model = PartnerStaff
        fields = ('id', 'partner', 'user', 'role', 'is_active', 'created_at', 'updated_at')
        export_order = fields


class PartnerProductResource(resources.ModelResource):
    partner = fields.Field(
        column_name='partner',
        attribute='partner',
        widget=ForeignKeyWidget(Partner, 'name')
    )
    herb = fields.Field(
        column_name='herb',
        attribute='herb',
        widget=ForeignKeyWidget('herbs.Herb', 'name')
    )

    class Meta:
        model = PartnerProduct
        fields = ('id', 'partner', 'herb', 'is_available', 'created_at', 'updated_at')
        export_order = fields


class PartnerReviewResource(resources.ModelResource):
    partner = fields.Field(
        column_name='partner',
        attribute='partner',
        widget=ForeignKeyWidget(Partner, 'name')
    )
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )

    class Meta:
        model = PartnerReview
        fields = ('id', 'partner', 'user', 'rating', 'comment', 'approved', 'created_at', 'updated_at')
        export_order = fields
