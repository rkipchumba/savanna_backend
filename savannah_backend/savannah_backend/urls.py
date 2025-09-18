from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet, CategoryViewSet
from orders.views import OrderViewSet
from django.urls import path, include
from django.contrib import admin
from customers.views import GoogleLogin
from . import views


router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", views.home, name="home"),

    # API routes
    path('api/', include(router.urls)),

    # Auth routes (dj-rest-auth)
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),

    # Allauth (for login, logout, signup, Google frontend)
    path("accounts/", include("allauth.urls")),  

    path("products/", include("products.urls")),
    path("orders/", include("orders.urls")),

]
