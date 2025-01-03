from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('', ProductViewSet, basename='products')

urlpatterns = router.urls 