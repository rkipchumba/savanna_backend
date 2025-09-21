from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.shortcuts import render



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def average_price(self, request, pk=None):
        """Return average price including all child categories."""
        category = self.get_object()

        categories = [category]
        children = list(category.children.all())
        while children:
            next_children = []
            for c in children:
                categories.append(c)
                next_children.extend(list(c.children.all()))
            children = next_children

        products = Product.objects.filter(category__in=categories)
        avg_price = products.aggregate(avg_price=Avg('price'))['avg_price']
        avg_price = round(avg_price, 2) if avg_price else 0

        return Response({
            "category": category.name,
            "average_price": avg_price
        })


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

def product_list(request):
    # Get all top-level categories
    categories = Category.objects.filter(parent=None).prefetch_related('children', 'products')
    
    category_data = []

    for category in categories:
        for child in category.children.all():
            # Compute average price for this category including its children
            all_products = Product.objects.filter(category__in=[child])
            avg_price = all_products.aggregate(avg_price=Avg('price'))['avg_price'] or 0

            # Truncate decimal by converting to int
            avg_price = int(avg_price)

            # Truncate individual product prices
            products = []
            for product in child.products.all():
                product.price = int(product.price)
                products.append(product)

            category_data.append({
                "id": child.id,
                "name": child.name,
                "products": products,
                "average_price": avg_price,
            })

    return render(request, "products/list.html", {"categories": category_data})
