from rest_framework import serializers

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff', 'is_superuser',
            'groups', 'user_permissions',
        )
