import os
from django.db import models
from django.utils.deconstruct import deconstructible
from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class BaseModel(models.Model):
    is_active = models.BooleanField(verbose_name=_('Active'), default=True)
    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True,
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated at'),
        auto_now=True,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__} (ID: {self.id}, Active: {self.is_active})"


@deconstructible
class UploadPath:
    def __init__(self, folder, sub_path):
        self.folder = folder
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        # Use os.path.splitext to handle file extensions safely
        _, extension = os.path.splitext(filename)
        extension = extension.lstrip('.')  # Remove the leading dot if present
        return f"{self.folder}/{self.sub_path}/{timestamp}.{extension}"


@deconstructible
class FileSizeValidator:
    message = _(
        "File size %(size)sMB exceeds the limit of %(max_size)sMB."
    )
    code = "file_too_large"

    def __init__(self, max_size_mb=20, message=None, code=None):
        self.max_size_mb = max_size_mb
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        size_mb = value.size / (1024 * 1024)
        if size_mb > self.max_size_mb:
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    "size": round(size_mb, 2),
                    "max_size": self.max_size_mb,
                    "value": value,
                },
            )

    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.max_size_mb == other.max_size_mb
                and self.message == other.message
                and self.code == other.code
        )


class SeoModel(models.Model):
    class TwitterCardTypeChoices(models.TextChoices):
        SUMMARY = "summary", _("Summary")
        SUMMARY_LARGE_IMAGE = "summary_large_image", _("Summary Large Image")
        APP = "app", _("App")
        PLAYER = "player", _("Player")

    class RobotsIndexChoices(models.TextChoices):
        INDEX = "index", _("Index")
        NOINDEX = "noindex", _("No Index")

    class RobotsFollowChoices(models.TextChoices):
        FOLLOW = "follow", _("Follow")
        NOFOLLOW = "nofollow", _("No Follow")

    meta_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Meta Title")
        )
    meta_description = models.TextField(blank=True, null=True, verbose_name=_("Meta Description"))
    meta_keywords = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        verbose_name=_("Meta Keywords")
        )
    canonical_url = models.URLField(blank=True, null=True, verbose_name=_("Canonical URL"))

    og_image = models.ImageField(
        upload_to=UploadPath("seo", "og"),
        blank=True,
        null=True,
        verbose_name=_("OG Image"),
        validators=[FileSizeValidator(max_size_mb=3)],
        help_text=_("Image for social media sharing."),
    )

    twitter_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Twitter Title")
        )
    twitter_description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Twitter Description")
        )
    twitter_card_type = models.CharField(
        max_length=32,
        choices=TwitterCardTypeChoices.choices,
        default=TwitterCardTypeChoices.SUMMARY_LARGE_IMAGE,
        blank=True,
        null=True,
        verbose_name=_("Twitter Card Type"),
    )

    robots_index = models.CharField(
        max_length=10,
        choices=RobotsIndexChoices.choices,
        default=RobotsIndexChoices.INDEX,
        verbose_name=_("Robots Index"),
        help_text=_("Should search engines index this page?"),
    )
    robots_follow = models.CharField(
        max_length=10,
        choices=RobotsFollowChoices.choices,
        default=RobotsFollowChoices.FOLLOW,
        verbose_name=_("Robots Follow"),
        help_text=_("Should search engines follow links on this page?"),
    )

    class Meta:
        abstract = True
