import africastalking
from django.conf import settings

def get_sms_service():
    """Initialize Africa's Talking and return SMS service only (sandbox-safe)"""
    africastalking.initialize(
        username=settings.AT_USERNAME,  # must be 'sandbox'
        api_key=settings.AT_API_KEY     # sandbox API key
    )
    return africastalking.SMS

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
