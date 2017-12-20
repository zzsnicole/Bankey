from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from .managers import UserManager


class Country(models.Model):
    """
    Country model
    """
    name = models.CharField(max_length=128, blank=False, null=False)
    code = models.CharField(max_length=128, unique=True, blank=False, null=False)
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    def __str__(self):
        country = '%s(%s)' % (self.name, self.code)
        return country.strip()

    def delete(self):
        """
        Delete currency
        """
        self.status = 'D'
        self.save()


class Address(models.Model):
    """
    Address model
    """
    line1 = models.CharField(max_length=128, blank=True, null=True)
    location = models.CharField(max_length=128, blank=True, null=True)
    city_or_village = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    # country = models.ForeignKey('Country', related_name='address', blank=False, null=False)
    country = models.CharField(max_length=128, blank=True, null=True)
    pin_code = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    def __str__(self):
        return self.country

    def delete(self):
        """
        Delete address
        """
        self.status = 'D'
        self.save()


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model
    """
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    phone_no = models.CharField(_('phone number'), validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:\
                                  '+999999999'. Up to 15 digits allowed.")], max_length=15,\
                                  unique=True, blank=False, null=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    photo = models.ImageField(upload_to='user_photos/', default='user_photos/no-photo.jpeg')
    address = models.ForeignKey('Address', related_name='user', blank=False, null=True)
    contacts = models.ManyToManyField('self', related_name='user_contacts', blank=True)
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_no']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def delete(self):
        """
        Delete user
        """
        self.status = 'D'
        self.save()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class PhoneVerification(models.Model):
    """
    VerificationCode model for phone number verification
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_phone_verification',\
                             blank=False, null=False)
    phone_no = models.CharField(_('phone number'), validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:\
                                  '+999999999'. Up to 15 digits allowed.")], max_length=15,\
                                  unique=True, blank=False, null=False)
    verified_on = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=64, unique=True, blank=False, null=False)
    status = models.CharField(max_length=1, choices=settings.VERIFICATION_STATUS, default='U')


class UserCardInfo(models.Model):
    """
    User's credit or debit cards information
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_card_info',\
                             blank=False, null=False)
    card_campany_name = models.CharField(max_length=128, blank=False, null=False)  #visa, master
    card_no = models.CharField(max_length=64, unique=True, blank=False, null=False)
    cvv = models.PositiveIntegerField(blank=False, null=False)
    expiry_date = models.CharField(max_length=7, blank=False, null=False) #month/year
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    def __str__(self):
        return self.card_no

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
    account_no = models.CharField(max_length=64, blank=False, null=False)
    bank_name = models.CharField(max_length=128, blank=True, null=True)
    branch_name = models.CharField(max_length=128, blank=True, null=True)
    IFSC = models.CharField(max_length=128, blank=False, null=False)
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    class Meta:
        unique_together = ('IFSC','account_no')

    def delete(self):
        """
        Delete user's bank account information
        """
        self.status = 'D'
        self.save()


class Teller(models.Model):
    """
    Teller model
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='teller')
    service_activation = models.BooleanField(
        _('Is Service Activate'),
        default=False,
        help_text=_('Is service activate for users.'),
    )

    def __str__(self):
        return self.user.email


class UserRatingsAndFeedback(models.Model):
    """
    User's rating and feedback information
    """
    teller = models.ForeignKey(Teller, related_name='user_ratings_and_feedback_from',\
                             blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_ratings_and_feedback_to',\
                             blank=False, null=False)
    datetime = models.DateTimeField(default=timezone.now)
    ratings = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    def delete(self):
        """
        Delete ratings and feedback for user
        """
        self.status = 'D'
        self.save()


class TellerRatingsAndFeedback(models.Model):
    """
    Teller's rating and feedback information
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_ratings_and_feedback_from',\
                             blank=False, null=False)
    teller = models.ForeignKey(Teller, related_name='user_ratings_and_feedback_to',\
                             blank=False, null=False)
    datetime = models.DateTimeField(default=timezone.now)
    ratings = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    def delete(self):
        """
        Delete ratings and feedback for teller
        """
        self.status = 'D'
        self.save()


class Service(models.Model):
    """
    Service model
    """
    name = models.CharField(max_length=128, blank=False, null=False)
    code = models.CharField(max_length=128, unique=True, blank=False, null=False)
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    def __str__(self):
        return self.name

    def delete(self):
        """
        Delete service
        """
        self.status = 'D'
        self.save()


class TellerServiceCharges(models.Model):
    """
    TellerServiceCharges model
    """
    teller = models.ForeignKey(Teller, related_name='teller_service_charges',\
                             blank=False, null=False)
    service = models.ForeignKey(Service, related_name='teller_service_charges',\
                             blank=False, null=False)
    min_charges = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False)
    max_charges = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False)

    class Meta:
        unique_together = ('teller','service')


class ChatMessages(models.Model):
    """
    ChatMessages model
    """
    datetime = models.DateTimeField()
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chat_message_from',\
                             blank=False, null=False)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chat_message_to',\
                             blank=False, null=False)
    message = models.TextField(null=False, blank=False)
