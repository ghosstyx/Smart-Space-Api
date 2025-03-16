from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException


class AccountNotRegisteredException(APIException):
    status_code = 404
    default_detail = {
        'detail': _('The account is not registered.'),
        'is_registered': False
    }
    default_code = 'non-registered-account'


class AccountDisabledException(APIException):
    status_code = 403
    default_detail = _('User account is disabled.')
    default_code = 'account-disabled'


class InvalidCredentialsException(APIException):
    status_code = 401
    default_detail = _('Wrong phone number or OTP.')
    default_code = 'invalid-credentials'
