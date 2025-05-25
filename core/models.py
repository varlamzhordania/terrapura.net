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
