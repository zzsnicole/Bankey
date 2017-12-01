from django.http import Http404

from user_management.models import *
from wallet_transactions.models import *
from .serializers import *
from user_management.rest.permissions import *

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status


class CurrencyViewSet(viewsets.ModelViewSet):
    """
    List, retrieve, add, update and delete currencies for bankey by admin only
    """
    queryset = Currency.objects.filter(status='A')
    serializer_class = CurrencySerializer
    permission_classes = (IsAdminUser,)


class SendMoneyTransactionHistoryViews(viewsets.ReadOnlyModelViewSet):
    """
    List and retrieve send_money transactions
    """
    queryset = SendMoneyTransactionHistory.objects.all()
    serializer_class = SendMoneyTransactionHistorySerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk):
        try:
            transaction = SendMoneyTransactionHistory.objects.get(pk=pk)
            serializer = SendMoneyTransactionHistorySerializer(transaction)
            return Response(serializer.data)
        except SendMoneyTransactionHistory.DoesNotExist:
            raise Http404


class WalletViewSet(viewsets.ViewSet):
    """
    User wallet list, retrieve, add and delete
    """
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = UserWallet.objects.filter(user=request.user)
        serializer = UserWalletSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = UserWallet.objects.filter(user=request.user)
        wallet = get_object_or_404(queryset, pk=pk)
        serializer = UserWalletSerializer(wallet)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            currency = Currency.objects.get(code=request.data['currency_code'])
            UserWallet.objects.create(user=request.user, currency=currency, balance=0)

            return Response({
                'success': True,
                'message': 'Wallet successfully created'
            })
        except Currency.DoesNotExist:
            raise Http404

    def put(self, request, format=None):
        pass

    def delete(self, request, format=None):

        try:
            wallet = UserWallet.objects.get(user=request.user, currency__code=request.data['currency_code'])
            wallet.delete()
            return Response({
                'success': True,
                'message': 'wallet deleted successfully'
            })
        except UserWallet.DoesNotExist:
            raise Http404


class ViewWalletBalance(APIView):
    """
    View wallet balance
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            wallet = UserWallet.objects.get(user=request.user, currency__code=request.data['currency_code'])
            serializer = UserWalletSerializer(wallet)
            return Response(serializer.data)
        except UserWallet.DoesNotExist:
            raise Http404


class TellerCashBalancesViewSet(viewsets.ViewSet):
    """
    TellerCashBalances list, retrieve, add, update and delete
    """
    permission_classes = (IsTellerUser)

    def list(self, request):
        queryset = TellerCashBalances.objects.filter(teller__user=request.user)
        serializer = TellerCashBalancesSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = TellerCashBalances.objects.filter(teller__user=request.user)
        teller_cash_balance = get_object_or_404(queryset, pk=pk)
        serializer = TellerCashBalancesSerializer(teller_cash_balance)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            teller = Teller.objects.get(user=request.user)
            currency = Currency.objects.get(code=request.data['currency_code'])
            TellerCashBalances.objects.create(teller=teller, currency=currency, balance=request.data['balance'])

            return Response({
                'success': True,
                'message': 'Successfully created'
            })
        except Teller.DoesNotExist:
            raise Http404
        except Currency.DoesNotExist:
            raise Http404

    def put(self, request, format=None):
        try:
            teller_cash_balance = TellerCashBalances.objects.get(teller__user=request.user,\
                                                                currency__code=request.data['currency_code'])
            teller_cash_balance.balance = request.data['balance']
            teller_cash_balance.save()
            return Response({
                'success': True,
                'message': 'Balance updated successfully'
            })
        except TellerCashBalances.DoesNotExist:
            raise Http404

    def delete(self, request, format=None):
        try:
            teller_cash_balance = TellerCashBalances.objects.get(teller__user=request.user,\
                                                                currency__code=request.data['currency_code'])
            teller_cash_balance.delete()
            return Response({
                'success': True,
                'message': 'Balance deleted successfully'
            })
        except TellerCashBalances.DoesNotExist:
            raise Http404


