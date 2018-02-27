import time, base64, six, uuid, imghdr

from django.core.files.base import ContentFile
from django.core.files.base import ContentFile

from rest_framework import serializers

from user_management.models import *
from .user import *


class TellerSerializer(serializers.ModelSerializer):
    """
    Teller Serializer
    """
    user = UserSerializer()

    class Meta:
        model = Teller
        fields = ('id','user', 'service_activation', 'fee', 'lat', 'long', 'ratings')


class ServiceSerializer(serializers.ModelSerializer):
    """
    Service Serializer
    """
    class Meta:
        model = Service
        fields = ('name', 'code', 'status')


class TellerServiceChargesSerializer(serializers.ModelSerializer):
    """
    TellerServiceCharges Serializer
    """
    class Meta:
        model = TellerServiceCharges
        fields = ('teller', 'service', 'min_charges', 'max_charges')


class UserRatingsAndFeedbackSerializer(serializers.ModelSerializer):
    """
    UserRatingsAndFeedback Serializer
    """
    class Meta:
        model = UserRatingsAndFeedback
        fields = ('teller', 'user', 'datetime', 'ratings', 'feedback', 'status')

