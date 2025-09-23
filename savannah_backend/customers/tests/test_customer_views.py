# customers/tests/test_customer_views.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

@pytest.mark.django_db
def test_google_login_url_resolves():
    """
    Test that the GoogleLogin view can be called without raising SocialApp.DoesNotExist.
    """
    # Ensure a Site exists
    site = Site.objects.get_current()

    # Create a mock SocialApp for Google
    social_app = SocialApp.objects.create(
        provider='google',
        name='Test Google App',
        client_id='fake-client-id',
        secret='fake-secret',
    )
    social_app.sites.add(site)  # attach to the current site

    client = APIClient()
    url = reverse("google_login")  # ensures urls.py has name="google_login"
    response = client.post(url, data={})
    
    # Complete real OAuth here, just check that it doesn't crash
    assert response.status_code in [400, 302]
    
