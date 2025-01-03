from rest_framework import serializers
from common.serializers import BaseModelSerializer
from .models import Cart, CartItem
from products.serializers import ProductSerializer

class CartItemSerializer(BaseModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.CharField(write_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'product_id', 'quantity',
                 'created_at', 'updated_at')

class CartSerializer(BaseModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'created_at', 'updated_at') 