import logging

from django.http import Http404
from django.db import transaction

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from mangopay.resources import NaturalUser, Wallet, CardRegistration

from user_management.models import *
from wallet_transactions.models import *
from wallet_transactions.rest.serializers.wallet import *


logger = logging.getLogger("wallets_log")


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


class AddMoneyByCardView(APIView):
    """
    Add money by card
    """
    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            try:
                currency = Currency.objects.get(code=request.data['currency'])
                card_detail = UserCardDetails.objects.get(user=request.user, currency=currency, is_completed = True)
            except UserCardDetails.DoesNotExist:
                return Response({
                    'success': True,
                    'message': 'Please complete card registration first for selected currency.',
                    'data': {}
                })
            card_registration = CardRegistration.get(card_detail.mangopay_card_registration_id)
            user_wallet = UserWallet.objects.get(user=request.user, currency=currency, status='A')
            wallet = Wallet.get(user_wallet.mangopay_wallet_id)
            mangopay_user = NaturalUser.get(request.user.mangopay_user_id)
            direct_payin = DirectPayIn(author=mangopay_user,
                                       debited_funds=Money(amount=request.data['amount'], currency=currency.code),
                                       fees=Money(amount=currency.fee, currency=currency.code),
                                       credited_wallet_id=wallet.get_pk(),
                                       card_id=card_registration.CardId,
                                       secure_mode="DEFAULT",
                                       secure_mode_return_url = "/") #take url from client

            direct_payin.save()
            logger.info("{} {} credited by {} user.".format(request.data['amount'], currency.code, request.user.phone_no))
            return Response({
                'success': True,
                'message': 'Money successfully credited.',
                'data': {
                    'transaction_id': direct_payin.get_pk()
                }
            })
        except Exception as e:
            logger.error("{}, error occured while adding money by card.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while adding money by card.',
                'data':{}
            })
