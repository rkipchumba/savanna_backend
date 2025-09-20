from .models import Order

def cart_item_count(request):
    if request.user.is_authenticated:
        customer = getattr(request.user, "customer_profile", None)
        if customer:
            order = Order.objects.filter(customer=customer, status="pending").first()
            count = order.items.count() if order else 0
            return {"cart_item_count": count}
    return {"cart_item_count": 0}
