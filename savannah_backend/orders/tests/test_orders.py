import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from products.models import Product, Category
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer
import json


@pytest.mark.django_db
def test_order_and_orderitem_str_and_properties():
    user = User.objects.create_user(username="john")
    customer = user.customer_profile
    cat = Category.objects.create(name="Books")
    product = Product.objects.create(name="Django Book", price=100, category=cat)
    order = Order.objects.create(customer=customer)
    item = OrderItem.objects.create(order=order, product=product, quantity=2)

    assert str(order) == f"Order {order.id} by {customer.user.username}"
    assert str(item) == "2 × Django Book"
    assert item.subtotal == 200
    assert order.total_price == 200


@pytest.mark.django_db
def test_orderitem_serializer_calculates_subtotal():
    user = User.objects.create_user(username="alice")
    customer = user.customer_profile
    cat = Category.objects.create(name="Electronics")
    product = Product.objects.create(name="Laptop", price=1000, category=cat)
    order = Order.objects.create(customer=customer)
    item = OrderItem.objects.create(order=order, product=product, quantity=3)

    ser = OrderItemSerializer(item)
    assert ser.data["subtotal"] == 3000


@pytest.mark.django_db
def test_order_serializer_total_price_and_create():
    user = User.objects.create_user(username="bob")
    customer = user.customer_profile
    cat = Category.objects.create(name="Toys")
    p1 = Product.objects.create(name="Toy A", price=50, category=cat)
    p2 = Product.objects.create(name="Toy B", price=30, category=cat)

    data = {
        "customer": customer.id,
        "items": [
            {"product_id": p1.id, "quantity": 2},
            {"product_id": p2.id, "quantity": 3},
        ]
    }

    ser = OrderSerializer(data=data)
    assert ser.is_valid(raise_exception=True)
    order = ser.save()
    assert order.total_price == 2*50 + 3*30
    assert order.items.count() == 2


@pytest.mark.django_db
def test_add_to_cart_and_cart_count():
    user = User.objects.create_user(username="cartuser")
    customer = user.customer_profile
    cat = Category.objects.create(name="Books")
    product = Product.objects.create(name="Book A", price=20, category=cat)

    client = Client()
    client.force_login(user)

    # Add to cart
    response = client.post(
        reverse("add_to_cart"),
        {"product_id": product.id, "quantity": 2}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["cart_count"] == 1

    # Cart count view
    response = client.get(reverse("cart_count"))
    assert response.status_code == 200
    assert response.json()["cart_count"] == 1


@pytest.mark.django_db
def test_update_and_remove_cart_item():
    user = User.objects.create_user(username="updateuser")
    customer = user.customer_profile
    cat = Category.objects.create(name="Books")
    product = Product.objects.create(name="Book B", price=10, category=cat)
    order = Order.objects.create(customer=customer)
    item = OrderItem.objects.create(order=order, product=product, quantity=1)

    client = Client()
    client.force_login(user)

    # Update quantity
    response = client.post(
        reverse("update_cart"),
        data=json.dumps({"item_id": item.id, "quantity": 5}),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["subtotal"] == 50
    assert data["total"] == 50
    assert data["cart_count"] == 1

    # Remove item
    response = client.post(
        reverse("remove_cart_item"),
        data=json.dumps({"item_id": item.id}),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["cart_count"] == 0
