from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts import serializers
from accounts.exceptions import InvalidCredentialsException
from accounts.otp_serice import generate_otp, verify_otp
from .models import NaturalPerson

User = get_user_model()


class RegistrationAPIView(GenericAPIView):
    """
    Register new users using phone number.
    """
    # serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        otp_code = request.data.get('otp')
        secret_code = request.data.get('secret')

        if verify_otp(secret_code, otp_code=otp_code):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.create(self.request.data)

            if user:
                refresh = RefreshToken.for_user(user)
                data = {
                    'detail': _('Successfully registration.'),
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            raise InvalidCredentialsException()


class LoginAPIView(GenericAPIView):
    """
    Authenticate existing users using phone number and password.
    """
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        user_data = serializers.UserSerializer(user).data
        data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': user_data
        }
        return Response(data, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    """
    Logout the user by blacklisting the provided refresh token.
    """
    serializer_class = serializers.LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh']
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)


class SendOTPAPIView(GenericAPIView):
    """
    Send OTP to the provided phone number.
    """
    serializer_class = serializers.PhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            secret_code, otp_code = generate_otp(str(phone_number))
            return Response(data={"secret": secret_code}, status=200)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
