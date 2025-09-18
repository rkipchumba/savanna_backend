from django.urls import path
from . import views

urlpatterns = [
    path("place/<int:product_id>/", views.place_order, name="place_order"),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
