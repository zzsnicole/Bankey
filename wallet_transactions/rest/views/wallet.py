import logging

from django.http import Http404
from django.db import transaction

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from mangopay.resources import NaturalUser, Wallet

from user_management.models import *
from wallet_transactions.models import *
from wallet_transactions.rest.serializers.wallet import *


logger = logging.getLogger("wallets_log")


class CurrencyListView(generics.ListAPIView):
    """
    List currencies
    """
    queryset = Currency.objects.filter(status='A')
    serializer_class = CurrencySerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            res = self.list(request, *args, **kwargs)
            logger.info("List of currencies are successfully retrieved.")
            return Response({
                'success': True,
                'message': 'List of currencies.',
                'data': res.data
            })
        except Exception as e:
            logger.error("{}, error occured while listing currencies.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while listing currencies.',
                'data':{}
            })


class CreateWallet(APIView):
    """
    Create wallet
    """
    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            try:
                currency = Currency.objects.get(code=request.data['currency'])
                UserWallet.objects.get(user=request.user, currency=currency, status='A')
                return Response({
                    'success': False,
                    'message': 'Wallet Exist.',
                    'data': {}
                })
            except UserWallet.DoesNotExist:
                mangopay_user = NaturalUser.get(request.user.mangopay_user_id)
                wallet = Wallet(owners=[mangopay_user], description="Bankey wallet", currency=currency.code)
                wallet.save()
                UserWallet.objects.create(user=request.user, currency=currency, mangopay_wallet_id=wallet.id)
                logger.info("{} wallet created successfully for {} currency.".format(request.user.phone_no, currency.code))
                return Response({
                    'success': True,
                    'message': 'Successfully wallet created',
                    'data': {}
                })
        except Exception as e:
            logger.error("{}, error occured while creating wallet.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while creating wallet.',
                'data':{}
            })


class GetWalletBalance(APIView):
    """
    Return wallet balance
    """
    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            currency = Currency.objects.get(code=request.data['currency'])
            user_wallet = UserWallet.objects.get(user=request.user, currency=currency, status='A')
            wallet = Wallet.get(user_wallet.mangopay_wallet_id)
            logger.info("Successfully returned balance of {} user for {} currency.".format(request.user.phone_no, currency.code))
            return Response({
                'success': True,
                'message': 'Successfully returned balance.',
                'data': {
                    "balance": str(wallet.balance.amount)
                }
            })
        except Exception as e:
            logger.error("{}, error occured while returning balance.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while returning balance.',
                'data':{}
            })
