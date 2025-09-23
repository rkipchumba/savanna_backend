import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from .models import Order, OrderItem
from .serializers import OrderSerializer
from customers.models import Customer
from products.models import Product
from utils.notifications import send_sms




class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # skip CSRF check

@login_required
def cart_count(request):
    customer = request.user.customer_profile
    order = Order.objects.filter(customer=customer, status="pending").first()
    count = order.items.count() if order else 0
    return JsonResponse({"cart_count": count})

@require_POST
def add_to_cart(request):
    """AJAX add to cart without redirect."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "not_authenticated"}, status=401)

    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("quantity", 1))

    product = get_object_or_404(Product, id=product_id)
    customer = request.user.customer_profile

    # Get first pending order, or create a new one if none exists
    order = Order.objects.filter(customer=customer, status="pending").first()
    if not order:
        order = Order.objects.create(customer=customer, status="pending")

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={"quantity": quantity}
    )
    if not created:
        order_item.quantity += quantity
        order_item.save()

    return JsonResponse({"success": True, "cart_count": order.items.count()})


def cart_view(request):
    """Display the user's pending cart."""
    if not request.user.is_authenticated:
        return redirect("account_login")

    customer = request.user.customer_profile
    order = Order.objects.filter(customer=customer, status="pending").first()
    items = []
    total = 0

    if order:
        for item in order.items.all():
            subtotal = int(item.product.price * item.quantity)  # truncate decimal
            total += subtotal
            # attach truncated subtotal to item for template
            item.subtotal_int = subtotal
            items.append(item)

    return render(request, "orders/cart.html", {"items": items, "total": total})


@require_POST
def checkout(request):
    """Marks pending order as completed and notifies admin."""
    if not request.user.is_authenticated:
        return redirect("account_login")

    customer = request.user.customer_profile
    order = Order.objects.filter(customer=customer, status="pending").first()
    if not order:
        return redirect("cart_view")

    # Complete the order
    order.status = "completed"
    order.save()

    # Calculate totals
    items = order.items.all()
    total_price = sum([i.product.price * i.quantity for i in items])

    # Prepare email/SMS content
    rows = "".join(
        f"<tr><td>{i.product.name}</td><td>{i.quantity}</td><td>{i.product.price}</td></tr>"
        for i in items
    )
    html_content = f"""
    <h2>New Order #{order.id} Placed</h2>
    <p><strong>Customer:</strong> {customer.user.get_full_name() or customer.user.username}<br>
    <strong>Phone:</strong> {customer.phone or 'Not provided'}<br>
    <strong>Total:</strong> {total_price}</p>
    <h3>Items:</h3>
    <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;">
      <tr><th>Product</th><th>Quantity</th><th>Price</th></tr>
      {rows}
    </table>
    """
    text_content = f"New order #{order.id} by {customer.user.get_full_name() or customer.user.username}. Total: {total_price}.\n" + \
                   "\n".join([f"{i.product.name} x {i.quantity} @ {i.product.price}" for i in items])

    # Send email
    subject = f"New Order #{order.id} Placed"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = ["kipchumbarodgers@gmail.com"]
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    # Send SMS (optional)
    if customer.phone:
        sms_message = f"Hi {customer.user.get_full_name() or customer.user.username}, your order #{order.id} has been placed successfully. Total: {total_price}."
        send_sms(customer.phone, sms_message)

    return render(request, "orders/order_success.html", {"order": order})


# DRF API views (optional, for API orders)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product").all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer_profile)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def place_order(request):
    """
    API endpoint to place an order with multiple products.
    Only for API/JS clients, not used for regular HTML add-to-cart.
    """
    customer = Customer.objects.get(user=request.user)
    items_data = request.data.get("items", [])
    if not items_data:
        return Response({"error": "No items provided"}, status=400)

    order = Order.objects.create(customer=customer)
    total = 0
    sms_lines = []

    for item in items_data:
        product = get_object_or_404(Product, id=item["product_id"])
        quantity = item.get("quantity", 1)
        OrderItem.objects.create(order=order, product=product, quantity=quantity)

        subtotal = product.price * quantity
        total += subtotal
        sms_lines.append(f"{product.name} x {quantity} = {subtotal}")

    # Send SMS (optional)
    if customer.phone:
        message = f"Hi {customer.user.get_full_name() or customer.user.username}, your order #{order.id} has been placed.\nDetails:\n" + "\n".join(sms_lines)
        send_sms(customer.phone, message)

    return Response({"message": f"Order {order.id} placed successfully", "total": total})


@csrf_exempt
@require_POST
def update_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "not_authenticated"}, status=401)

    data = json.loads(request.body)
    item_id = data.get("item_id")
    quantity = int(data.get("quantity", 1))

    item = get_object_or_404(
        OrderItem,
        id=item_id,
        order__customer=request.user.customer_profile,
        order__status="pending"
    )
    item.quantity = quantity
    item.save()

    order = item.order
    total = sum(i.product.price * i.quantity for i in order.items.all())
    cart_count = order.items.count()

    return JsonResponse({
        "success": True,
        "subtotal": int(item.product.price * item.quantity),
        "total": int(total),
        "cart_count": cart_count  # <-- add this
    })


@csrf_exempt
@require_POST
def remove_cart_item(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "not_authenticated"}, status=401)

    data = json.loads(request.body)
    item_id = data.get("item_id")
    item = get_object_or_404(
        OrderItem,
        id=item_id,
        order__customer=request.user.customer_profile,
        order__status="pending"
    )
    order = item.order
    item.delete()

    total = sum(i.product.price * i.quantity for i in order.items.all())
    cart_count = order.items.count()

    return JsonResponse({
        "success": True,
        "total": int(total),
        "cart_count": cart_count 
    })


@login_required
def orders_list(request):
    """Display all completed orders for the current user."""
    customer = request.user.customer_profile
    orders = Order.objects.filter(customer=customer, status="completed").prefetch_related("items__product")
    
    # Compute totals for each order
    orders_data = []
    for order in orders:
        total = sum(int(item.product.price * item.quantity) for item in order.items.all())
        orders_data.append({"order": order, "total": total})

    return render(request, "orders/orders_list.html", {"orders_data": orders_data})
