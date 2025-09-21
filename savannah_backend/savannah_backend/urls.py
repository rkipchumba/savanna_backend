from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet, CategoryViewSet
from orders.views import OrderViewSet
from django.urls import path, include
from django.contrib import admin
from . import views

# DRF router
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet)  # /api/orders/

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # API routes
    path('api/', include(router.urls)),

    # Auth routes
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),

    # Allauth frontend login/logout/signup
    path('accounts/', include('allauth.urls')),

    # Frontend app routes
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),

    # Test SMS endpoint
    path('test-sms/', views.test_sms, name='test_sms'),
]
