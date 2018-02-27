from rest_framework import serializers

from wallet_transactions.models import *
from user_management.rest.serializers.teller import *
from wallet_transactions.rest.serializers.wallet import *


class CashRequestSerializer(serializers.ModelSerializer):
    """
    Cash Request Serializer
    """
    teller = TellerSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = CashRequest
        fields = ('id', 'request_datetime', 'currency', 'amount', 'user', 'teller', 'user_confirmation_code',\
                  'request_type', 'request_status', 'note', 'transaction_reference_number')