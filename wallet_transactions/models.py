from django.db import models
from django.conf import settings
from django.utils import timezone

from user_management.models import User, Teller, Country


class Currency(models.Model):
    """
    Currency model
    """
    name = models.CharField(max_length=128, blank=False, null=False)
    code = models.CharField(max_length=128, unique=True, blank=False, null=False)
    fee = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=True)
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

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
    mangopay_wallet_id = models.CharField(max_length=256, blank=False, null=True)
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
    request_datetime = models.DateTimeField(default=timezone.now)
    currency = models.ForeignKey(Currency, related_name='cash_request',\
                             blank=False, null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cash_request',\
                             blank=False, null=False)
    teller = models.ForeignKey(Teller, related_name='cash_request',\
                             blank=False, null=False)
    user_confirmation_code = models.CharField(max_length=128, unique=True, blank=True, null=True)

    note = models.CharField(max_length=1024, blank=True, null=True)

    transaction_reference_number = models.CharField(max_length=32, blank=False, null=True)

    request_type = models.CharField(max_length=1, choices=settings.CASH_REQUEST_TYPE, null=True)

    request_status = models.CharField(max_length=1, choices=settings.CASH_REQUEST_STATUS, default='P')


class CashTransactionHistory(models.Model):
    """
    CashTransactionHistory model
    """
    request = models.ForeignKey(CashRequest, related_name='cash_transaction',\
                             blank=False, null=False)
    # transaction = models.ForeignKey(Transaction, related_name='cash_transaction',\
    #                          blank=False, null=False)
    transaction_reference_no = models.CharField(max_length=256, unique=True, blank=True, null=False)
    teller_confirmation_code = models.CharField(max_length=128, unique=True, blank=True, null=False)


class UserCardInfo(models.Model):
    """
    User's credit or debit cards information
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_card_info',\
                             blank=False, null=False)
    card_type = models.CharField(max_length=64, blank=False, null=False)  #visa or master
    card_no = models.BigIntegerField(unique=True, blank=False, null=False)
    cvv = models.PositiveSmallIntegerField(blank=False, null=False)
    expiry_month = models.PositiveSmallIntegerField(blank=False, null=False)
    expiry_year =  models.PositiveSmallIntegerField(blank=False, null=False)
    stripe_card_token = models.CharField(max_length=64, blank=False, null=True)
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    def __str__(self):
        card = '%s - %s' % (self.card_type, self.card_no)
        return card.strip()

    def delete(self):
        """
        Delete user's card information
        """
        self.status = 'D'
        self.save()


class UserBankInfo(models.Model):
    """
    User's banks information
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_bank_info',\
                             blank=False, null=False)
    account_no = models.BigIntegerField(blank=False, null=False)
    routing_number = models.CharField(max_length=128, blank=False, null=False)
    account_type = models.CharField(max_length=64, blank=False, null=False, default='individual') #individual or company or joint
    country = models.ForeignKey(Country, related_name='user_bank_country', blank=False, null=False)
    currency = models.ForeignKey('Currency', related_name='user_bank_currency',blank=False, null=False)
    stripe_bank_token = models.CharField(max_length=64, blank=False, null=True)
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    class Meta:
        unique_together = ('user', 'routing_number', 'account_no')

    def __str__(self):
        account = '%s - %s' % (self.account_no, self.routing_number)
        return account.strip()

    def delete(self):
        """
        Delete user's bank account information
        """
        self.status = 'D'
        self.save()


class CardTransactionHistory(models.Model):
    """
    CardTransactionHistory model
    """
    user_card = models.ForeignKey('UserCardInfo', related_name='card_transaction',\
                             blank=False, null=False)
    transaction = models.ForeignKey(Transaction, related_name='card_transaction',\
                             blank=False, null=False)


class NetBankingTransactionHistory(models.Model):
    """
    NetBankingTransactionHistory model
    """
    user_bank = models.ForeignKey('UserBankInfo', related_name='net_banking_transaction',\
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


class UserCardDetails(models.Model):
    """
    User's credit or debit cards information
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_card_details',\
                             blank=False, null=False)
    currency = models.ForeignKey(Currency, related_name='user_card_details',\
                             blank=False, null=False)
    mangopay_card_registration_id = models.CharField(max_length=128, blank=False, null=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user','currency')

    def __str__(self):
        card = '%s - %s' % (self.currency, self.mangopay_card_registration_id)
        return card.strip()
