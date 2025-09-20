from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('get_price', 'subtotal')

    def get_price(self, obj):
        return obj.product.price
    get_price.short_description = "Price"

    def subtotal(self, obj):
        return obj.product.price * obj.quantity
    subtotal.short_description = "Subtotal"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price', 'created_at', 'product_details')
    inlines = [OrderItemInline]
    readonly_fields = ('total_price',)

    # This method must be inside OrderAdmin
    def product_details(self, obj):
        items = list(obj.items.all())  # force evaluation to avoid cursor errors
        if not items:
            return "-"
        return ", ".join(
            f"{item.product.name} (Price: {item.product.price}, Qty: {item.quantity}, Subtotal: {item.product.price * item.quantity})"
            for item in items
        )
    product_details.short_description = "Products"

    # Prefetch products to avoid extra queries
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('items__product')
