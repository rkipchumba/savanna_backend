# tests/test_notifications.py
import pytest
from unittest.mock import patch, MagicMock
from utils.notifications import get_sms_service, send_sms

@pytest.mark.django_db
@patch("africastalking.initialize")
def test_get_sms_service(mock_initialize, settings):
    # Patch settings
    settings.AT_USERNAME = "testuser"
    settings.AT_API_KEY = "testkey"

    # Patch africastalking.SMS to a mock class
    with patch("africastalking.SMS") as MockSMS:
        instance = MockSMS.return_value
        service = get_sms_service()
        MockSMS.assert_called_once()
        mock_initialize.assert_called_once_with(username="testuser", api_key="testkey")
        assert service == instance

@patch("utils.notifications.get_sms_service")
def test_send_sms_success(mock_get_sms):
    mock_sms_instance = MagicMock()
    mock_sms_instance.send.return_value = {"status": "Success"}
    mock_get_sms.return_value = mock_sms_instance

    send_sms("+254700000000", "Hello World")
    mock_sms_instance.send.assert_called_once_with("Hello World", ["+254700000000"])

@patch("utils.notifications.get_sms_service")
def test_send_sms_failure(mock_get_sms):
    mock_sms_instance = MagicMock()
    mock_sms_instance.send.side_effect = Exception("Network error")
    mock_get_sms.return_value = mock_sms_instance

    send_sms("+254700000000", "Hello World")
    mock_sms_instance.send.assert_called_once_with("Hello World", ["+254700000000"])
