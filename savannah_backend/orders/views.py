from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import get_object_or_404

from .models import Order, OrderItem
from .serializers import OrderSerializer
from customers.models import Customer
from products.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product").all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Assumes Customer is linked to User via OneToOneField
        serializer.save(customer=self.request.user.customer_profile)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # skip CSRF check


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Assumes Customer has a OneToOne relation with User
    customer = Customer.objects.get(user=request.user)

    # Create order and order item
    order = Order.objects.create(customer=customer)
    OrderItem.objects.create(order=order, product=product, quantity=1)

    return Response({"message": f"Order {order.id} placed for {product.name}"})
