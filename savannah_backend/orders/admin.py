from django.contrib import admin
from django.utils.html import format_html, format_html_join
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'get_price', 'quantity', 'subtotal')

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

    def product_details(self, obj):
        items = obj.items.all()
        if not items:
            return "-"
        return ", ".join(
        f"{item.product.name} (Price: {item.product.price}, Qty: {item.quantity}, Subtotal: {item.product.price * item.quantity})"
        for item in items
    )

    product_details.short_description = "Products"
