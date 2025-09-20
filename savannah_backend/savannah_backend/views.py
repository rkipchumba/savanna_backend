from django.http import JsonResponse
from django.shortcuts import render
from utils.notifications import send_sms

def home(request):
    return render(request, "base.html")

def test_sms(request):
    phone = "254711111111" 
    message = "Hello! This is a test SMS from Savannah Backend."
    send_sms(phone, message)
    return JsonResponse({"status": "SMS sent (check console/logs for response)"})
