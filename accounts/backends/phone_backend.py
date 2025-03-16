from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from accounts.otp_serice import verify_otp


User = get_user_model()


class PhoneNumberAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, secret='', otp='', password=None):
        try:
            user = User.objects.get(phone_number=username)
            if user.is_staff and user.check_password(password):
                return user
            elif user and verify_otp(secret, otp):
                return user
        except User.DoesNotExist:
            return
