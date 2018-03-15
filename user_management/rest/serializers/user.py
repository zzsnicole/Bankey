"""
Serializers for user_management app
"""
import time, base64, six, uuid, imghdr

from django.core.files.base import ContentFile
from django.core.files.base import ContentFile

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from mangopay.resources import NaturalUser, Wallet

from user_management.models import *
from wallet_transactions.models import *


class Base64ImageField(serializers.ImageField):
    """
    Base64ImageField
    """
    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
            	header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    """
    User Photo Serializer
    """
    phone_no = serializers.CharField(required=False, allow_blank=False, max_length=128)
    photo = Base64ImageField(
        max_length=None, use_url=False,
    )

    class Meta:
        model = User
        fields = ('photo','phone_no')


class CountrySerializer(serializers.ModelSerializer):
    """
    Country Serializer
    """
    class Meta:
        model = Country
        fields = ('name', 'code', 'std_code', 'flag', 'status')


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
        # read_only_fields = ('photo',)

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        user = User.objects.create(**validated_data)
        country = Country.objects.get(code=address_data['country'])
        user.address = Address.objects.create(country=country)
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        first_name, last_name = validated_data['name'].split(' ')
        birth_date = int(time.mktime(time.strptime(str(validated_data['birth_date']),'%Y-%m-%d')))
        mangopay_user = NaturalUser(first_name=first_name,
                                   last_name=last_name,
                                   birthday=birth_date,
                                   nationality=country.code,
                                   country_of_residence=country.code,
                                   person_type='NATURAL',
                                   email=validated_data['email'])
        mangopay_user.save()
        user.mangopay_user_id = mangopay_user.id
        user.save()
        wallet = Wallet(owners=[mangopay_user],
                        description='Wallet for USD',
                        currency='USD')

        wallet.save()
        currency = Currency.objects.get(code='USD')
        UserWallet.objects.create(user=user, currency=currency, mangopay_wallet_id= wallet.id)
        return user

    def update(self, instance, validated_data):
        mangopay_user = NaturalUser.get(instance.mangopay_user_id)
        print(">>>>>",mangopay_user.id)
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        # instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        mangopay_user.email = instance.email
        mangopay_user.birthday = int(time.mktime(time.strptime(str(instance.birth_date),'%Y-%m-%d')))
        mangopay_user.first_name, mangopay_user.last_name = instance.name.split(' ')
        print(instance.email, type(instance.email), int(time.mktime(time.strptime(str(instance.birth_date),'%Y-%m-%d'))),\
              type(int(time.mktime(time.strptime(str(instance.birth_date),'%Y-%m-%d')))))
        address_data = validated_data.pop('address')
        address = instance.address
        address.line1 = address_data.get('line1', address.line1)
        mangopay_user.address.address_line_1 = address_data.get('line1', address.line1)
        address.line2 = address_data.get('line2', address.line2)
        mangopay_user.address.address_line_2 = address_data.get('line2', address.line2)
        address.city = address_data.get('city', address.city)
        mangopay_user.address.city = address_data.get('city', address.city)
        address.state = address_data.get('state', address.state)
        mangopay_user.address.region = address_data.get('state', address.state)
        address.country = Country.objects.get(code=address_data.get('country', address.country))
        mangopay_user.address.country = address_data.get('country', address.country)
        address.pin_code = address_data.get('pin_code', address.pin_code)
        mangopay_user.address.postal_code = address_data.get('pin_code', address.pin_code)
        address.save()
        mangopay_user.save()
        return instance


class UserEditSerializer(serializers.ModelSerializer):
    """
    User Edit Serializer
    """
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ('address',)
        read_only_fields = ('email', 'phone_no', 'password', 'name', 'date_joined','birth_date',\
                  'contacts', 'status', 'is_staff', 'is_superuser', 'photo',)

    def update(self, instance, validated_data):
        mangopay_user = NaturalUser.get(instance.mangopay_user_id)
        print(">>>>>",mangopay_user.id)
        address_data = validated_data.pop('address')
        address = instance.address
        address.line1 = address_data.get('line1', address.line1)
        mangopay_user.address.address_line_1 = address_data.get('line1', address.line1)
        address.line2 = address_data.get('line2', address.line2)
        mangopay_user.address.address_line_2 = address_data.get('line2', address.line2)
        address.city = address_data.get('city', address.city)
        mangopay_user.address.city = address_data.get('city', address.city)
        address.state = address_data.get('state', address.state)
        mangopay_user.address.region = address_data.get('state', address.state)
        address.country = Country.objects.get(code=address_data.get('country', address.country))
        mangopay_user.address.country = address_data.get('country', address.country)
        address.pin_code = address_data.get('pin_code', address.pin_code)
        mangopay_user.address.postal_code = address_data.get('pin_code', address.pin_code)
        address.save()
        mangopay_user.save()
        return instance


class UserContactsSerializer(serializers.ModelSerializer):
    """
    UserContacts Serializer
    """
    class Meta:
        model = User
        fields = ('phone_no', 'photo')


class TellerRatingsAndFeedbackSerializer(serializers.ModelSerializer):
    """
    TellerRatingsAndFeedback Serializer
    """
    class Meta:
        model = TellerRatingsAndFeedback
        fields = ('teller', 'user', 'datetime', 'ratings', 'feedback', 'status')
