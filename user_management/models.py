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
    std_code = models.CharField(max_length=128, unique=True, blank=False, null=False)
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
    line2 = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    country = models.ForeignKey('Country', related_name='address', blank=False, null=False)
    pin_code = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    def __str__(self):
        return self.country.code

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
    phone_no = models.CharField(_('mobile number'), validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:\
                                  '+999999999'. Up to 15 digits allowed.")], max_length=15,\
                                  unique=True, blank=False, null=False)
    email = models.EmailField(_('email address'), blank=True, null=True)
    name = models.CharField(_('name'), max_length=30, blank=False, null=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    photo = models.ImageField(upload_to='user_photos/', default='user_photos/no-photo.jpeg')
    address = models.ForeignKey('Address', related_name='user', blank=False, null=True)
    birth_date = models.DateField('Birth Date', blank=True, null=True)
    contacts = models.ManyToManyField('self', related_name='user_contacts', blank=True)
    status = models.CharField(max_length=1, choices=settings.STATUS_CHOICES, default='A')

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.phone_no

    def get_short_name(self):
        return self.name

    def delete(self):
        """
        Delete user
        """
        self.status = 'D'
        self.save()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class PhoneVerification(models.Model):
    """
    VerificationCode model for phone number verification
    """
    phone_no = models.CharField(_('phone number'), validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:\
                                  '+999999999'. Up to 15 digits allowed.")], max_length=15,\
                                  unique=True, blank=False, null=False)
    code = models.PositiveIntegerField(unique=True, blank=False, null=False)
    verified_on = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, choices=settings.VERIFICATION_STATUS, default='U')


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
