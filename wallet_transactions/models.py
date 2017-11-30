from django.db import models
from django.conf import settings

from user_management.models import Teller, UserCardInfo, UserBankInfo


class Currency(models.Model):
    """
    Currency model
    """
    name = models.CharField(max_length=128, blank=False, null=False)
    code = models.CharField(max_length=128, unique=True, blank=False, null=False)
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    def __str__(self):
        currency = '%s(%s)' % (self.name, self.code)
        return currency.strip()

    def delete(self):
        """
        Delete currency
        """
        self.status = 'D'
        self.save()


class UserWallet(models.Model):
    """
    UserWallet model
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='userwallet',\
                             blank=False, null=False)
    currency = models.ForeignKey(Currency, related_name='userwalletcurrency',\
                             blank=False, null=False)
    balance = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False)
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    class Meta:
        unique_together = ('user','currency')

    def __str__(self):
        return self.user.email

    def delete(self):
        """
        Delete user's wallet
        """
        self.status = 'D'
        self.save()


class Transaction(models.Model):
    """
    Transaction model
    """
    transaction_datetime = models.DateTimeField()
    currency = models.ForeignKey(Currency, related_name='transaction',\
                             blank=False, null=False)
    amount = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False)
    transaction_type = models.CharField(max_length=1, choices=settings.TRANSACTION_TYPES)
    transaction_status = models.CharField(max_length=1, choices=settings.TRANSACTION_STATUS)


class CashRequest(models.Model):
    """
    CashRequest model
    """
    request_datetime = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cash_request',\
                             blank=False, null=False)
    teller = models.ForeignKey(Teller, related_name='cash_request',\
                             blank=False, null=False)
    request_status = models.CharField(max_length=1, choices=settings.CASH_REQUEST_STATUS)


class CashTransactionHistory(models.Model):
    """
    CashTransactionHistory model
    """
    request = models.ForeignKey(CashRequest, related_name='cash_transaction',\
                             blank=False, null=False)
    transaction = models.ForeignKey(Transaction, related_name='cash_transaction',\
                             blank=False, null=False)
    teller_confirmation_code = models.CharField(max_length=128, blank=True, null=False)


class CardTransactionHistory(models.Model):
    """
    CardTransactionHistory model
    """
    user_card = models.ForeignKey(UserCardInfo, related_name='card_transaction',\
                             blank=False, null=False)
    transaction = models.ForeignKey(Transaction, related_name='card_transaction',\
                             blank=False, null=False)


class NetBankingTransactionHistory(models.Model):
    """
    NetBankingTransactionHistory model
    """
    user_bank = models.ForeignKey(UserBankInfo, related_name='net_banking_transaction',\
                             blank=False, null=False)
    transaction = models.ForeignKey(Transaction, related_name='net_banking_transaction',\
                             blank=False, null=False)


class SendMoneyTransactionHistory(models.Model):
    """
    SendMoneyTransactionHistory model
    """
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='send_money_transaction_from',\
                             blank=False, null=False)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='send_money_transaction_to',\
                             blank=False, null=False)
    transaction = models.ForeignKey(Transaction, related_name='send_money_transaction',\
                             blank=False, null=False)
    note = models.TextField(null=True, blank=True)


class TellerCashBalances(models.Model):
    """
    TellerServiceCharges model
    """
    teller = models.ForeignKey(Teller, related_name='teller_cash_balances',\
                             blank=False, null=False)
    currency = models.ForeignKey(Currency, related_name='teller_cash_currency',\
                             blank=False, null=False)
    balance = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False)

    class Meta:
        unique_together = ('teller','currency')
