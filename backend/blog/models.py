import json
from urllib.parse import urljoin

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from django_ckeditor_5.fields import CKEditor5Field

from core.models import BaseModel, SeoModel, UploadPath, FileSizeValidator

User = get_user_model()


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Category Name"))
    slug = AutoSlugField(populate_from="name", unique=True, verbose_name=_("Slug"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Tag Name"))
    slug = AutoSlugField(populate_from="name", unique=True, verbose_name=_("Slug"))

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(SeoModel, BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = AutoSlugField(populate_from="title", unique=True, editable=True, verbose_name=_("Slug"))
    excerpt = CKEditor5Field(verbose_name=_("Excerpt"), blank=True, null=True)
    content = CKEditor5Field(verbose_name=_("Content"))
    thumbnail = models.ImageField(
        upload_to=UploadPath("blog", "thumbnails"),
        blank=True,
        null=True,
        verbose_name=_("Thumbnail"),
        validators=[FileSizeValidator(max_size_mb=5)],
    )
    author_user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Author User"),
        help_text=_("if author is a user of platform"),
        related_name="posts",
    )
    author = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Author Name"),
        help_text=_("if real author is someone else"),
    )
    category = models.ForeignKey(
        Category,
        related_name="posts",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Category")
    )
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True, verbose_name=_("Tags"))
    related_herbs = models.ManyToManyField(
        "herbs.Herb",
        related_name="blog_posts",
        blank=True,
        verbose_name=_("Related Herbs")
    )
    publish_date = models.DateTimeField(blank=True, null=True, verbose_name=_("Publish Date"))
    is_active = models.BooleanField(default=False, verbose_name=_("Published"))

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ["-publish_date", "-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["publish_date"]),
        ]

    def __str__(self):
        return self.title

    @property
    def display_author(self):
        return self.author or (
            self.author_user.get_full_name() if self.author_user else "Anonymous")

    def get_structured_data(self, frontend_base_url: str) -> str:
        """
        Returns JSON-LD structured data, using the frontend base URL.
        """
        post_url = urljoin(frontend_base_url, f"/blog/{self.slug}/")

        return json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "BlogPosting",
                "headline": self.meta_title or self.title,
                "image": urljoin(frontend_base_url, self.og_image.url) if self.og_image else "",
                "author": {
                    "@type": "Person",
                    "name": self.display_author,
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Terrapura",
                    "logo": {
                        "@type": "ImageObject",
                        "url": urljoin(frontend_base_url, "/static/logo.png")
                    }
                },
                "datePublished": self.publish_date.isoformat() if self.publish_date else "",
                "description": self.meta_description or "",
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": post_url
                }
            }, ensure_ascii=False
        )


class Comment(BaseModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Post")
    )
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    email = models.EmailField(verbose_name=_("Email"))
    message = models.TextField(verbose_name=_("Comment"))
    is_active = models.BooleanField(default=False, verbose_name=_("Approved"))

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.post.title[:30]}"
