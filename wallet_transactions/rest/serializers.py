"""
Serializers for wallet_transactions app
"""
from wallet_transactions.models import *
from rest_framework import serializers


class UserWalletSerializer(serializers.ModelSerializer):
    """
    UserWallet Serializer
    """
    class Meta:
        model = UserWallet
        fields = ('user', 'currency', 'balance','status')


class TellerCashBalancesSerializer(serializers.ModelSerializer):
    """
    TellerCashBalances Serializer
    """
    class Meta:
        model = TellerCashBalances
        fields = ('teller', 'currency', 'balance')


class SendMoneyTransactionHistorySerializer(serializers.ModelSerializer):
    """
    SendMoneyTransactionHistory Serializer
    """
    class Meta:
        model = SendMoneyTransactionHistory
        fields = ('from_user', 'to_user', 'transaction', 'note')
