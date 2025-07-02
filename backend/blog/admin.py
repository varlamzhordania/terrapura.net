from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from reversion.admin import VersionAdmin
from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from import_export.admin import ExportMixin

from .models import Post, Category, Tag, Comment
from .resources import PostResource, CategoryResource, TagResource, CommentResource


@admin.register(Post)
class PostAdmin(ExportMixin, VersionAdmin):
    resource_class = PostResource
    list_display = (
        'title', 'display_author', 'category', 'is_active', 'publish_date', 'created_at')
    list_filter = ('is_active', 'category', 'tags', 'publish_date', 'created_at')
    search_fields = ('title', 'excerpt', 'content', 'author', 'author_user__email')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags', 'related_herbs')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('Main Info'), {
            'fields': ('title', 'slug', 'excerpt', 'content', 'thumbnail')
        }),
        (_('Author Info'), {
            'fields': ('author_user', 'author')
        }),
        (_('Classification'), {
            'fields': ('category', 'tags', 'related_herbs')
        }),
        (_('Publication'), {
            'fields': ('publish_date', 'is_active')
        }),
        (_('SEO Settings'), {
            'classes': ('collapse',),
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords',
                'canonical_url', 'og_image',
                'twitter_title', 'twitter_description', 'twitter_card_type',
                'robots_index', 'robots_follow',
            )
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(Category)
class CategoryAdmin(ExportMixin, VersionAdmin):
    resource_class = CategoryResource
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(ExportMixin, VersionAdmin):
    resource_class = TagResource
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(ExportMixin, VersionAdmin):
    resource_class = CommentResource
    list_display = ('name', 'email', 'post', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'message', 'post__title')
    readonly_fields = ('created_at', 'updated_at')
