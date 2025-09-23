import pytest
from products.models import Category, Product
from products.serializers import ProductSerializer, CategorySerializer

@pytest.mark.django_db
def test_product_serializer_serializes_correctly():
    cat = Category.objects.create(name="Books")
    product = Product.objects.create(name="Python Book", price=150.50, category=cat)
    serializer = ProductSerializer(product)
    data = serializer.data
    assert data['name'] == "Python Book"
    assert float(data['price']) == 150.50
    assert data['category'] == cat.id

@pytest.mark.django_db
def test_category_serializer_recursive_and_average_price():
    parent = Category.objects.create(name="Electronics")
    child = Category.objects.create(name="Phones", parent=parent)
    p1 = Product.objects.create(name="iPhone", price=1000, category=child)
    p2 = Product.objects.create(name="Samsung", price=800, category=child)

    serializer = CategorySerializer(parent)
    data = serializer.data

    # Recursive children
    assert len(data['children']) == 1
    assert data['children'][0]['name'] == "Phones"

    # Average price including children
    avg_price = (1000 + 800) / 2
    assert data['average_price'] == avg_price
