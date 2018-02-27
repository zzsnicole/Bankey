import logging
import random, string

from django.http import Http404
from django.db import transaction

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from mangopay.resources import NaturalUser, Wallet

from user_management.models import *
from wallet_transactions.models import *
from wallet_transactions.rest.serializers.offline_transactions import *


logger = logging.getLogger("wallets_log")


class CreateCashRequestView(APIView):
    """
    Create cash request by user to teller
    """
    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            teller = Teller.objects.get(id=request.data['teller_id'])
            currency = Currency.objects.get(code=request.data['currency'])
            cash_request = CashRequest.objects.create(user=request.user, teller=teller,\
                                                      currency=currency, note=request.data['note'],\
                                                      amount=decimal.Decimal(request.data['amount']),\
                                                      request_type=request.data['transaction_mode'])
            cash_request_serializer = CashRequestSerializer(cash_request)
            logger.info("Cash_request sent by {} user to {} teller.".format(request.user.phone_no, teller.user.phone_no))
            return Response({
                'success': True,
                'message': 'Cash request successfully raised.',
                'data':cash_request_serializer.data
            })
        except Exception as e:
            logger.error("{}, error occured while cash request.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while cash request.',
                'data':{}
            })


class CashRequestDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update cash request
    """
    queryset = CashRequest.objects.all()
    serializer_class = CashRequestSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'success': True,
                'message': 'Successfully displayed details.',
                'data':serializer.data
            })
        except Exception as e:
            logger.error("{}, error occured while displaying teller details.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while displaying teller details.',
                'data': {}
            })

    @transaction.atomic()
    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.request_status == 'P':
                instance.request_status = request.data['request_status']
            elif instance.request_status == 'A':
                if request.data['is_confirm']:
                    instance.user_confirmation_code = ''.join([random.choice(string.digits) for n in range(6)])
                else:
                    instance.request_status = 'R'
            instance.note = request.data['note']
            instance.save()
            cash_request_serializer = CashRequestSerializer(instance)
            logger.info("{} cash_request is updated successfully.".format(instance.id))
            return Response({
                'success': True,
                'message': 'Successfully updated.',
                'data': cash_request_serializer.data
            })
        except Exception as e:
            logger.error("{}, error occured while updating cash request.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while updating cash request.',
                'data':{}
            })


class CashTransactionView(APIView):
    """
    Cash transaction between user and teller
    """
    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            cash_request = CashRequest.objects.get(user_confirmation_code=request.data['confirmation_code'])
            teller = Teller.objects.get(user=request.user)
            if cash_request.teller == teller:
                teller_wallet_obj = UserWallet.objects.get(user=request.user, currency=cash_request.currency, status='A')
                teller_wallet = Wallet.get(teller_wallet_obj.mangopay_wallet_id)
                user_wallet_obj = UserWallet.objects.get(user=cash_request.user, currency=cash_request.currency, status='A')
                user_wallet = Wallet.get(user_wallet_obj.mangopay_wallet_id)
                if cash_request.request_type == 'A':
                    transaction_amount = cash_request.amount - teller.fee
                    author_user = NaturalUser.get(request.user.mangopay_user_id)
                    transfer = Transfer(author=author_user, #sender
                                        debited_funds=Money(amount=transaction_amount, currency=cash_request.currency.code),
                                        fees=Money(amount=cash_request.currency.fee, currency=cash_request.currency.code),
                                        debited_wallet=teller_wallet,
                                        credited_wallet=user_wallet)
                else:
                    transaction_amount = cash_request.amount + teller.fee + cash_request.currency.fee
                    author_user = NaturalUser.get(cash_request.user.mangopay_user_id)
                    transfer = Transfer(author=author_user, #sender
                                        debited_funds=Money(amount=transaction_amount, currency=cash_request.currency.code),
                                        fees=Money(amount=cash_request.currency.fee, currency=cash_request.currency.code),
                                        debited_wallet=user_wallet,
                                        credited_wallet=teller_wallet)
                transfer.save()
            cash_request.transaction_reference_number = transfer.get_pk()
            cash_request.save()
            logger.info("Cash_transaction completed successfully  between {} user and {} teller for {} cashrequest."\
                        .format(request.user.phone_no, teller.user.phone_no, cash_request.id))
            return Response({
                'success': True,
                'message': 'Cash transaction successfully completed.',
                'data':{
                    'transaction_id':transfer.get_pk()
                }
            })
        except Exception as e:
            logger.exception("{}, error occured while cash transaction.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while cash transaction.',
                'data':{}
            })


class TransferTransactionView(APIView):
    """
    Send money from one user to another
    """
    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            currency = Currency.objects.get(code=request.data['currency'])
            receiver_user = User.objects.get(phone_no=request.data['mobile_number'])
            sender_wallet_obj = UserWallet.objects.get(user=request.user, currency=currency, status='A')
            sender_wallet = Wallet.get(sender_wallet_obj.mangopay_wallet_id)
            receiver_wallet_obj = UserWallet.objects.get(user=receiver_user, currency=currency, status='A')
            receiver_wallet = Wallet.get(receiver_wallet_obj.mangopay_wallet_id)
            author_user = NaturalUser.get(request.user.mangopay_user_id)
            transfer = Transfer(author=author_user, #sender
                                debited_funds=Money(amount=request.data['amount'], currency=currency.code),
                                fees=Money(amount=currency.fee, currency=currency.code),
                                debited_wallet=sender_wallet,
                                credited_wallet=receiver_wallet)

            transfer.save()
            logger.info("Money transfered successfully from {} user to {} user."\
                        .format(request.user.phone_no, receiver_user.phone_no))
            return Response({
                'success': True,
                'message': 'Money transfered successfully.',
                'data':{
                    'transaction_id':transfer.get_pk()
                }
            })
        except Exception as e:
            logger.exception("{}, error occured while transfering money.".format(e))
            return Response({
                'success': False,
                'message': 'Error occured while transfering money.',
                'data':{}
            })


