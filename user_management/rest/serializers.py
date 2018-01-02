"""
Serializers for user_management app
"""
from user_management.models import *
from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer):
    """
    Country Serializer
    """
    class Meta:
        model = Country
        fields = ('name', 'code', 'std_code', 'status')


class AddressSerializer(serializers.ModelSerializer):
    """
    Address Serializer
    """
    country = serializers.CharField(required=False, allow_blank=False, max_length=128)

    class Meta:
        model = Address
        fields = ('line1', 'line2', 'city', 'state', 'country', 'pin_code')


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ('email', 'phone_no', 'password', 'name', 'date_joined','birth_date',\
                  'address', 'contacts', 'status', 'is_staff', 'is_superuser', 'photo')

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        user = User.objects.create(**validated_data)
        country = Country.objects.get(code=address_data['country'])
        user.address = Address.objects.create(line1=address_data['line1'], line2=address_data['line2'],\
                                              city=address_data['city'], state=address_data['state'], country=country,\
                                              pin_code=address_data['pin_code'])
        user.set_password(validated_data['password'])
        user.save()
        Teller.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        address = instance.address
        address_data = validated_data.pop('address')
        address.line1 = address_data.get('line1', address.line1)
        address.line2 = address_data.get('line2', address.line2)
        address.city = address_data.get('city', address.city)
        address.state = address_data.get('state', address.state)
        address.country = Country.objects.get(code=address_data.get('country', address.country))
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
