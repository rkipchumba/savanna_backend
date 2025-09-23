# customers/tests/test_customer_serializer.py
import pytest
from django.contrib.auth.models import User
from customers.models import Customer
from customers.serializers import CustomerSerializer

@pytest.mark.django_db
def test_customer_serializer_serializes_correctly():
    # Create a user
    user = User.objects.create_user(username="user1", email="user1@example.com", first_name="John", last_name="Doe", password="pass")
    
    # Customer is automatically created via signal
    customer = Customer.objects.get(user=user)
    
    serializer = CustomerSerializer(customer)
    data = serializer.data

    # Check that serialized data includes correct values
    assert data["id"] == customer.id
    assert data["name"] == user.get_full_name()  # "John Doe"
    assert data["email"] == user.email
    assert data["phone"] is None  # phone defaults to None

@pytest.mark.django_db
def test_customer_serializer_deserialization():
    # Create a user
    user = User.objects.create_user(username="user2", email="user2@example.com", password="pass")
    
    # Prepare data for updating Customer
    data = {"phone": "123456789"}  # Only phone is writable
    customer = Customer.objects.get(user=user)
    
    serializer = CustomerSerializer(customer, data=data, partial=True)
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    
    # Ensure phone was updated
    assert instance.phone == "123456789"
