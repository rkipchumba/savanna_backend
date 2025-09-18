import africastalking
from django.conf import settings

# Initialize SDK
username = settings.AT_USERNAME 
api_key = settings.AT_API_KEY

africastalking.initialize(username, api_key)
sms = africastalking.SMS
