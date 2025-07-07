from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from core.mixins import OptionalPaginationMixin
from herbs.models import (
    Herb,
    Category,
    Tag,
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
