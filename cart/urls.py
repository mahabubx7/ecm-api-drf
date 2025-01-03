from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register('items', CartItemViewSet, basename='cart-items')
router.register('', CartViewSet, basename='cart')

urlpatterns = router.urls 