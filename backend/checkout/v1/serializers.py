from rest_framework import serializers

from checkout.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['code', 'name', 'symbol']
