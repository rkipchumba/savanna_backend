from rest_framework import serializers
from django.db.models import Avg
from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category']


class RecursiveField(serializers.Serializer):
    """Helper serializer to handle recursive Category children."""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, required=False)
    products = ProductSerializer(many=True, read_only=True)
    average_price = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'children', 'products', 'average_price']

    def get_average_price(self, obj):
        # Recursive function to gather all products from category and children
        def gather_products(category):
            products = list(category.products.all())
            for child in category.children.all():
                products += gather_products(child)
            return products

        products = gather_products(obj)
        if not products:
            return None
        total = sum(p.price for p in products)
        return round(total / len(products), 2)
