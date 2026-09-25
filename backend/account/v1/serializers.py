from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from account.models import User, Address


class UserSerializer(serializers.ModelSerializer):
    partner_staff = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'phone_number',
            'date_joined', 'is_staff', 'is_superuser',
            'groups', 'partner_staff',
        )

    def get_partner_staff(self, obj):
        staff_roles = obj.partner_roles.filter(is_active=True)
        if not staff_roles.exists():
            return None
        return [
            {
                "partner_id": staff.partner_id,
                "partner_name": staff.partner.name,
                "role": staff.role,
            }
            for staff in staff_roles
        ]


class UserSettingsSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
        ]
        read_only_fields = ["email"]


class AddressSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(required=True)

    class Meta:
        model = Address
        fields = "__all__"


class ListAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'id',
            'full_name',
            'phone_number',
            'line1',
            'line2',
            'city',
            'state',
            'postal_code',
            'country',
            'is_default',
        )


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                _("User with this email does not exist.")
            )
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        try:
            validate_password(value)  # runs Django’s password validators
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError(_('Invalid user or UID.'))

        if not PasswordResetTokenGenerator().check_token(
                user,
                attrs['token']
        ):
            raise serializers.ValidationError(
                _('Invalid or expired token.')
            )

        # everything valid → reset password
        user.set_password(attrs['new_password'])
        user.save()

        attrs['user'] = user  # return user if needed
        return attrs
