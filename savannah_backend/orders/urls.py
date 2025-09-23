from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.cart_view, name="cart_view"),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update-cart/", views.update_cart, name="update_cart"),
    path("remove-cart-item/", views.remove_cart_item, name="remove_cart_item"),
    path("cart/count/", views.cart_count, name="cart_count"),
    path("", views.orders_list, name="orders_list"),

    

]

