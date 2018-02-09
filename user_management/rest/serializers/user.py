"""
Serializers for user_management app
"""
import time, base64, six, uuid, imghdr

from django.core.files.base import ContentFile
from django.core.files.base import ContentFile

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user_management.models import *


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
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        # instance.photo = validated_data.get('photo', instance.photo)
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
        fields = ('phone_no', 'photo')


class TellerRatingsAndFeedbackSerializer(serializers.ModelSerializer):
    """
    TellerRatingsAndFeedback Serializer
    """
    class Meta:
        model = TellerRatingsAndFeedback
        fields = ('teller', 'user', 'datetime', 'ratings', 'feedback', 'status')
