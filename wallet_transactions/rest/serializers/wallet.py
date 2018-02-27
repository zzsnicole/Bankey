from rest_framework import serializers

from wallet_transactions.models import *


class CurrencySerializer(serializers.ModelSerializer):
    """
    Currency Serializer
    """

    class Meta:
        model = Currency
        fields = ('name', 'code', 'fee', 'status')