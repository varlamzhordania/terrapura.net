from django_filters import rest_framework as filters

from herbs.models import Herb


class HerbFilter(filters.FilterSet):
    category = filters.BaseInFilter(field_name='category__slug', lookup_expr='in')
    tags = filters.BaseInFilter(field_name='tags__slug', lookup_expr='in')
    symptoms = filters.BaseInFilter(field_name='symptoms__slug', lookup_expr='in')

    class Meta:
        model = Herb
        fields = ['category', 'tags', 'symptoms']
