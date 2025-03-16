from django.conf import settings
from accounts.sms_service import send_sms
import pyotp


OTP_INTERVAL = settings.OTP_INTERVAL


def generate_otp(phone):
    interval = int(OTP_INTERVAL) if OTP_INTERVAL else 120
    secret_code = pyotp.random_base32()
    totp = pyotp.TOTP(secret_code, interval=interval)
    otp_code = totp.now()
    send_sms(phone_number=phone.replace("+", ""), message=f"Your secret code: {otp_code}")
    return secret_code, otp_code


def verify_otp(secret, otp_code):
    if otp_code == '111111':
        return True # TODO Поправить на проде!
    try:
        totp = pyotp.TOTP(secret, interval=int(OTP_INTERVAL))
        check = totp.verify(otp=otp_code, valid_window=3)
        return check
    except Exception:
        return False
