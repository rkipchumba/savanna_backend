import africastalking
from django.conf import settings

def get_sms_service():
    africastalking.initialize(
        username=settings.AT_USERNAME,
        api_key=settings.AT_API_KEY
    )
    return africastalking.SMS()

def send_sms(phone_number, message):
    """
    Send an SMS via Africa's Talking sandbox
    :param phone_number: E.g. "+2547XXXXXXXX" (must be registered in sandbox)
    :param message: Text message to send
    """
    try:
        sms = get_sms_service()
        response = sms.send(message, [phone_number])
        print("SMS sent:", response)
    except Exception as e:
        print("Failed to send SMS:", e)
