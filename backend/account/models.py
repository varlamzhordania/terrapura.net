from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=True, unique=True)
    last_ip = models.GenericIPAddressField(verbose_name=_("Last IP Address"), null=True, blank=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        if not self.first_name and not self.last_name:
            return self.username
        return f"{self.first_name} {self.last_name}"
