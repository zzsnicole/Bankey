"""
Serializers for user_management app
"""
from user_management.models import *
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    """
    Address Serializer
    """
    class Meta:
        model = Address
        fields = ('line1', 'location', 'city_or_village', 'state', 'country', 'pin_code')


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ('email', 'phone_no', 'password', 'first_name', 'last_name', 'date_joined',\
                  'address', 'contacts', 'status', 'is_staff', 'is_superuser', 'photo')

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        user = User.objects.create(**validated_data)
        user.address = Address.objects.create(**address_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        address = instance.address
        address_data = validated_data.pop('address')
        address.line1 = address_data.get('line1', address.line1)
        address.location = address_data.get('location', address.location)
        address.city_or_village = address_data.get('city_or_village', address.city_or_village)
        address.state = address_data.get('state', address.state)
        address.country = address_data.get('country', address.country)
        address.pin_code = address_data.get('pin_code', address.pin_code)
        address.save()
        return instance


class UserContactsSerializer(serializers.ModelSerializer):
    """
    UserContacts Serializer
    """
    class Meta:
        model = User
        fields = ('email', 'phone_no', 'photo')


class TellerSerializer(serializers.ModelSerializer):
    """
    Teller Serializer
    """
    user = UserSerializer()

    class Meta:
        model = Teller
        fields = ('user', 'service_activation')


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


class TellerRatingsAndFeedbackSerializer(serializers.ModelSerializer):
    """
    TellerRatingsAndFeedback Serializer
    """
    class Meta:
        model = TellerRatingsAndFeedback
        fields = ('teller', 'user', 'datetime', 'ratings', 'feedback', 'status')
