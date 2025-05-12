import re

# from allauth.account.views import email
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# from dj_rest_auth.registration.serializers import RegisterSerializer
from .exceptions import InvalidCredentialsException, AccountDisabledException


User = get_user_model()


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        pattern = r'^\+?1?\d{9,15}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                _("Phone number must be entered in the format: '+99999999999'. Up to 15 digits is allowed.")
            )
        return value


class LoginSerializer(PhoneNumberSerializer):
    secret = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, validated_data):
        phone_number = validated_data.get('phone', '')
        email = validated_data.get('email', '')
        secret = validated_data.get('secret')
        otp = validated_data.get('otp')

        user = authenticate(username=phone_number, secret=secret, otp=otp)

        if not user:
            raise InvalidCredentialsException()

        if not user.is_active:
            raise AccountDisabledException()

        validated_data['user'] = user
        return validated_data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
