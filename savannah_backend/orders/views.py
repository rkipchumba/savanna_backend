from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import get_object_or_404
from utils.notifications import send_sms
from django.core.mail import send_mail
from django.conf import settings


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
def place_order(request):
    """
    Place an order with multiple products at once.
    Expects request.data = {"items": [{"product_id": 1, "quantity": 2}, ...]}
    """
    customer = Customer.objects.get(user=request.user)

    items_data = request.data.get("items", [])
    if not items_data:
        return Response({"error": "No items provided"}, status=400)

    # Create the order
    order = Order.objects.create(customer=customer)

    sms_lines = []
    total = 0

    # Create order items
    for item in items_data:
        product = get_object_or_404(Product, id=item["product_id"])
        quantity = item.get("quantity", 1)
        OrderItem.objects.create(order=order, product=product, quantity=quantity)

        subtotal = product.price * quantity
        total += subtotal
        sms_lines.append(f"{product.name} x {quantity} = {subtotal}")

    # Send SMS notification
    if customer.phone:
        message = (
            f"Hi {customer.user.get_full_name() or customer.user.username}, "
            f"your order #{order.id} has been placed successfully.\n"
            f"Details:\n" + "\n".join(sms_lines) + f"\nTotal: {total}"
        )
        send_sms(customer.phone, message)

    # Send Email to Admin
    admin_email = "kipchumbarodgers@gmail.com"
    subject = f"New Order #{order.id} Placed"
    email_message = f"""
Hello Admin,

A new order has been placed:

Order ID: {order.id}
Customer: {customer.user.get_full_name() or customer.user.username}
Phone: {customer.phone or 'Not provided'}
Created At: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}

Order Details:
{chr(10).join(sms_lines)}

Total Price: {total}

Regards,
Savannah Backend
"""
    send_mail(
        subject,
        email_message,
        settings.DEFAULT_FROM_EMAIL,
        [admin_email],
        fail_silently=False,
    )

    return Response({"message": f"Order {order.id} placed successfully", "total": total})
    """
    Place an order with multiple products at once.
    Expects request.data = {"items": [{"product_id": 1, "quantity": 2}, ...]}
    """
    customer = Customer.objects.get(user=request.user)

    items_data = request.data.get("items", [])
    if not items_data:
        return Response({"error": "No items provided"}, status=400)

    # Create the order
    order = Order.objects.create(customer=customer)

    sms_lines = []
    total = 0

    # Create order items
    for item in items_data:
        product = get_object_or_404(Product, id=item["product_id"])
        quantity = item.get("quantity", 1)
        order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity)

        subtotal = product.price * quantity
        total += subtotal
        sms_lines.append(f"{product.name} x {quantity} = {subtotal}")

    # Send SMS notification
    if customer.phone:
        message = (
            f"Hi {customer.user.get_full_name() or customer.user.username}, "
            f"your order #{order.id} has been placed successfully.\n"
            f"Details:\n" + "\n".join(sms_lines) + f"\nTotal: {total}"
        )
        send_sms(customer.phone, message)

    return Response({"message": f"Order {order.id} placed successfully", "total": total})
