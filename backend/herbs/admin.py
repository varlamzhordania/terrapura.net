from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from reversion.admin import VersionAdmin
from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from import_export.admin import ExportMixin

from .models import (
    Category,
    Herb,
    HerbPreparationStep,
    HerbWarning,
    ScientificStudy,
    Ailment,
    SideEffect,
    Symptom,
    Illness,
    Source,
    Tag,
    HerbMedia,
)
from .resources import (
    CategoryResource,
    HerbResource,
    HerbPreparationStepResource,
    HerbWarningResource,
    ScientificStudyResource,
    AilmentResource,
    SideEffectResource,
    SymptomResource,
    IllnessResource,
    SourceResource,
    TagResource,
)


class HerbPreparationStepInline(NestedStackedInline):
    model = HerbPreparationStep
    extra = 1
    sortable_field_name = "order"
    fields = ('name', 'type', 'description', 'duration', 'temperature', 'order')
    ordering = ('order',)


class HerbWarningInline(NestedStackedInline):
    model = HerbWarning
    extra = 1
    sortable_field_name = "order"
    fields = ('name', 'type', 'description', 'order')
    ordering = ('order',)


class ScientificStudyInline(NestedStackedInline):
    model = ScientificStudy
    extra = 0
    fields = ('title', 'description', 'doi', 'pubmed_id', 'link')
    ordering = ('title',)


class HerbMediaInline(NestedTabularInline):
    model = HerbMedia
    extra = 1
    fields = ('file', 'type')


@admin.register(Category)
class CategoryAdmin(ExportMixin, VersionAdmin):
    resource_class = CategoryResource
    list_display = ('name', 'slug', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Herb)
class HerbAdmin(ExportMixin, NestedModelAdmin, VersionAdmin):
    resource_class = HerbResource
    list_display = ('name', 'latin_name', 'slug', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'latin_name', 'description')
    list_filter = ('tags', 'ailments', 'is_active', 'created_at', 'updated_at')
    filter_horizontal = ('ailments', 'side_effects', 'symptoms', 'illnesses', 'sources', 'tags')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

    inlines = [
        HerbPreparationStepInline,
        HerbWarningInline,
        ScientificStudyInline,
        HerbMediaInline,
    ]

    fieldsets = (
        (_('Basic Info'), {
            'fields': (
                'name', 'slug', 'latin_name', 'category', 'description', 'dosage', 'image_link',
                'is_active')
        }),
        (_('Relations'), {
            'fields': ('ailments', 'side_effects', 'symptoms', 'illnesses', 'sources', 'tags'),
        }),
        (_('SEO'), {
            'classes': ('collapse',),
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords',
                'canonical_url', 'og_image',
                'twitter_title', 'twitter_description', 'twitter_card_type',
                'robots_index', 'robots_follow'
            )
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at',)
        }),
    )


@admin.register(HerbPreparationStep)
class HerbPreparationStepAdmin(ExportMixin, VersionAdmin):
    resource_class = HerbPreparationStepResource
    list_display = ('herb', 'name', 'type', 'order', 'is_active', 'created_at', 'updated_at')
    list_filter = ('type', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('herb', 'order')


@admin.register(HerbWarning)
class HerbWarningAdmin(ExportMixin, VersionAdmin):
    resource_class = HerbWarningResource
    list_display = ('herb', 'name', 'type', 'order', 'is_active', 'created_at', 'updated_at')
    list_filter = ('type', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('herb', 'order')


@admin.register(ScientificStudy)
class ScientificStudyAdmin(ExportMixin, VersionAdmin):
    resource_class = ScientificStudyResource
    list_display = ('herb', 'title', 'doi', 'pubmed_id', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'doi', 'pubmed_id')
    ordering = ('herb', 'title')


@admin.register(Ailment)
class AilmentAdmin(ExportMixin, VersionAdmin):
    resource_class = AilmentResource
    list_display = ('name', 'slug', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SideEffect)
class SideEffectAdmin(ExportMixin, VersionAdmin):
    resource_class = SideEffectResource
    list_display = ('name', 'slug', 'severity', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Symptom)
class SymptomAdmin(ExportMixin, VersionAdmin):
    resource_class = SymptomResource
    list_display = ('name', 'slug', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Illness)
class IllnessAdmin(ExportMixin, VersionAdmin):
    resource_class = IllnessResource
    list_display = ('name', 'slug', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('ailments', 'symptoms')


@admin.register(Source)
class SourceAdmin(ExportMixin, VersionAdmin):
    resource_class = SourceResource
    list_display = ('name', 'url', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'url', 'description')


@admin.register(Tag)
class TagAdmin(ExportMixin, VersionAdmin):
    resource_class = TagResource
    list_display = ('name', 'slug', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
