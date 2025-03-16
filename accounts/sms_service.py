from decouple import config
from eskiz_sms import EskizSMS
from accounts.models import LogSms


def send_sms(message, phone_number):
    client = EskizSMS(email='m32iweokdskm', password='yacheeby')
    # resp = client.send_sms(
    #     mobile_phone=phone_number,
    #     message=message,
    #     from_whom='4546',
    #     callback_url=None
    # ) # TODO: Поправить на проде!
    resp = 'test'
    try:
        LogSms.objects.create(
            phone_number=phone_number,
            message=message,
            resp=f"{resp}"
        )
    except:
        pass
