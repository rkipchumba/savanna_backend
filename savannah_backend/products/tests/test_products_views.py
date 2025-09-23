import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.test import RequestFactory
from products.models import Category, Product
from products.views import product_list, CategoryViewSet, ProductViewSet
from rest_framework import status
from django.contrib.auth.models import AnonymousUser
from django.test import Client


@pytest.mark.django_db
def test_average_price_action():
    parent = Category.objects.create(name="Electronics")
    child1 = Category.objects.create(name="Laptops", parent=parent)
    child2 = Category.objects.create(name="Phones", parent=parent)

    Product.objects.create(name="Laptop A", price=1000, category=child1)
    Product.objects.create(name="Laptop B", price=2000, category=child1)
    Product.objects.create(name="Phone A", price=500, category=child2)

    client = APIClient()
    url = reverse('category-average-price', args=[parent.id])
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Electronics"
    assert data["average_price"] == 1166.67


@pytest.mark.django_db
def test_product_list_view_renders_correctly():
    parent = Category.objects.create(name="Books")
    child = Category.objects.create(name="Fiction", parent=parent)
    Product.objects.create(name="Book A", price=299.99, category=child)
    Product.objects.create(name="Book B", price=499.99, category=child)

    client = Client()
    response = client.get("/products/")  # Make sure this URL exists in urls.py
    assert response.status_code == 200

    # Use `response.context` instead of context_data
    categories = response.context["categories"]
    assert len(categories) == 1
    cat_data = categories[0]
    assert cat_data["name"] == "Fiction"
    # Prices should be truncated integers
    assert all(isinstance(p.price, int) for p in cat_data["products"])
    assert cat_data["average_price"] == 399

@pytest.mark.django_db
def test_product_viewset_list_and_retrieve():
    client = APIClient()
    cat = Category.objects.create(name="Gadgets")
    product = Product.objects.create(name="Smartwatch", price=150, category=cat)

    # List
    url = reverse('product-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Retrieve
    url = reverse('product-detail', args=[product.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["name"] == "Smartwatch"
