from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.OrderViewSet, basename='order')

urlpatterns = [
    # DRF router for API
    path('api/', include(router.urls)),

    # Your frontend/cart views
    path("cart/", views.cart_view, name="cart_view"),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("checkout/", views.checkout, name="checkout"),
]
