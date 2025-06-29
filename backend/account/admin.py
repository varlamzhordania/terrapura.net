from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        "id", "email", "is_staff", "is_superuser", "is_active", "date_joined",
        "last_login")
    list_filter = ("is_staff", "is_active", "groups")
    readonly_fields = ("date_joined", "last_login", "last_ip")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Information",
         {"fields": ("first_name", "last_name",)}),
        ("Permissions",
         {"fields": ("is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
        ("Security", {"fields": ("date_joined", "last_login", "last_ip")}),
    )
    add_fieldsets = (
        (None, {
            "fields": (
                "email", "password1", "password2", "first_name", "last_name",
                "groups", "is_staff", "is_active",
            )}
         ),
    )
    search_fields = ("id", "email",)
    ordering = ("id",)


admin.site.register(User, CustomUserAdmin)
