import logging

from django.http import Http404
from django.db import transaction

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from mangopay.resources import NaturalUser, Wallet, CardRegistration

from user_management.rest.permissions import *
from user_management.models import *
from wallet_transactions.models import *
from wallet_transactions.rest.serializers.wallet import *


logger = logging.getLogger("wallets_log")


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


class PreCardRegistrationView(APIView):
    """
    Pre Card Registration
    """
    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            try:
                card_detail = UserCardDetails.objects.get(user=request.user, currency__code=request.data['currency'])
                if card_detail.is_completed:
                    return Response({
                        'success': False,
                        'message': 'Card already registrated for given currency.',
                        'data': {}
                    })
                else:
                    card_registration = CardRegistration.get(card_detail.mangopay_card_registration_id)

            except UserCardDetails.DoesNotExist:
                mangopay_user = NaturalUser.get(request.user.mangopay_user_id)
                currency = Currency.objects.get(code=request.data['currency'])
                card_registration = CardRegistration(user=mangopay_user, currency=currency.code)
                card_registration.save()
                UserCardDetails.objects.create(user=request.user, currency=currency, \
                                                 mangopay_card_registration_id=card_registration.id)
            logger.info("Card successfully pre-registered for {} currency by {} user.".format(request.data['currency'],\
                                                                                                request.user.phone_no))
            return Response({
                'success': True,
                'message': 'Pre card registration successful.',
                'data': {
                    "AccessKey": card_registration.AccessKey,
                    "PreregistrationData": card_registration.PreregistrationData,
                    "CardRegistrationURL": card_registration.CardRegistrationURL
                }
            })
        except Exception as e:
            logger.exception("{}, error occured while pre card registration.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while pre card registration.',
                'data':{}
            })


class CardRegistrationView(APIView):
    """
    Card Registration
    """
    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            card_detail = UserCardDetails.objects.get(user=request.user, currency__code=request.data['currency'],\
                                                                                                is_completed = False)
            card_registration = CardRegistration.get(card_detail.mangopay_card_registration_id)
            card_registration.registration_data = request.data['registration_data']
            card_registration.save()
            card_detail.is_completed = True
            card_detail.save()
            logger.info("Card successfully registered for {} currency by {} user.".format(request.data['currency'],\
                                                                                                request.user.phone_no))
            return Response({
                'success': True,
                'message': 'card registration successful.',
                'data': {}
            })
        except Exception as e:
            logger.error("{}, error occured while card registration.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while card registration.',
                'data':{}
            })
