from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import get_object_or_404, redirect, render
from utils.notifications import send_sms
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST


from .models import Order, OrderItem
from .serializers import OrderSerializer
from customers.models import Customer
from products.models import Product

@require_POST
def checkout(request):
    """
    Marks the user's pending order as completed.
    Triggers post_save signals for notifications.
    """
    if not request.user.is_authenticated:
        return redirect("login")  # Redirect anonymous users to login

    customer = request.user.customer_profile
    order = Order.objects.filter(customer=customer, status="pending").first()

    if not order:
        # No pending order
        return redirect("cart_view")

    # Mark order as completed
    order.status = "completed"
    order.save()  # This triggers your post_save signal for notifications

    return render(request, "orders/order_success.html", {"order": order})


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

@require_POST
def add_to_cart(request):
    if not request.user.is_authenticated:
        return redirect("account_login")

    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("quantity", 1))

    product = get_object_or_404(Product, id=product_id)
    customer = request.user.customer_profile

    # Only get/create a pending order
    order, created = Order.objects.get_or_create(customer=customer, status="pending")

    # Add/update the item in the order
    order_item, item_created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={"quantity": quantity}
    )

    if not item_created:
        order_item.quantity += quantity
        order_item.save()

    return redirect("cart_view")

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect("account_login")

    customer = request.user.customer_profile
    order = Order.objects.filter(customer=customer, status="pending").first()
    items = order.items.all() if order else []
    total = sum(item.product.price * item.quantity for item in items) if order else 0

    return render(request, "orders/cart.html", {"items": items, "total": total})
