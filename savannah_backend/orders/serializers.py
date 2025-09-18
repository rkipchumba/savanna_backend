from rest_framework import serializers
from .models import Order
from products.serializers import ProductSerializer
from products.models import Product

class OrderSerializer(serializers.ModelSerializer):
    # Use nested ProductSerializer for read operations
    products = ProductSerializer(many=True, read_only=True)
    # Accept product IDs for creating an order
    product_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all(), write_only=True
    )
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'customer', 'products', 'product_ids', 'total_price', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        product_ids = validated_data.pop('product_ids')
        order = Order.objects.create(**validated_data)
        order.products.set(product_ids)
        # Calculate total price
        total = sum([p.price for p in product_ids])
        order.total_price = total
        order.save()
        return order
