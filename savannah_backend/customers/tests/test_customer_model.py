
import pytest
from django.contrib.auth.models import User
from customers.models import Customer

@pytest.mark.django_db
class TestCustomerModel:

    def test_customer_created_via_signal(self):
        """Ensure a Customer is automatically created when a User is created."""
        user = User.objects.create_user(username="user_signal_test", password="pass")
        customer = Customer.objects.get(user=user)
        assert customer is not None
        assert customer.user == user

    def test_customer_str_returns_full_name_or_username(self):
        """Ensure __str__ returns full name if set, else username."""
        user1 = User.objects.create_user(username="user1", password="pass")
        user1.first_name = "John"
        user1.last_name = "Doe"
        user1.save()
        customer1 = Customer.objects.get(user=user1)
        assert str(customer1) == "John Doe"

        user2 = User.objects.create_user(username="user2", password="pass")
        customer2 = Customer.objects.get(user=user2)
        assert str(customer2) == "user2"

    def test_customer_phone_field_optional(self):
        """Phone can be blank or null."""
        user = User.objects.create_user(username="user_phone_test", password="pass")
        customer = Customer.objects.get(user=user)
        assert customer.phone is None
        customer.phone = "123456789"
        customer.save()
        assert Customer.objects.get(user=user).phone == "123456789"
