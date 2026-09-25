from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Address


class AddressInline(admin.StackedInline):
    model = Address
    fieldsets = [
        ('Contact', {
            'fields': [
                'full_name', 'phone_number',
            ],
        }),
        ('Address', {
            'fields': [
                'line1',
                'line2',
                'country',
                'state',
                'city',
                'postal_code',
            ]
        }),
        ('Meta', {
            'fields': [
                'is_default',
                'is_active',
                'created_at',
                'updated_at',
            ]
        })
    ]
    readonly_fields = ['created_at', 'updated_at']
    extra = 0


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        "id", "email", "is_staff", "is_superuser", "is_active",
        "date_joined",
        "last_login")
    list_filter = ("is_staff", "is_active", "groups")
    readonly_fields = ("email", "date_joined", "last_login", "last_ip")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Information",
         {"fields": ("first_name", "last_name", "phone_number")}),
        ("Permissions",
         {"fields": ("is_staff", "is_superuser", "is_active", "groups",
                     "user_permissions")}),
        ("Security", {"fields": ("date_joined", "last_login", "last_ip")}),
    )
    add_fieldsets = (
        (None, {
            "fields": (
                "email", "password1", "password2", "first_name",
                "last_name", "phone_number",
                "groups", "is_staff", "is_active",
            )}
         ),
    )
    search_fields = ("id", "email",)
    ordering = ("id",)
    inlines = (AddressInline,)


admin.site.register(User, CustomUserAdmin)
