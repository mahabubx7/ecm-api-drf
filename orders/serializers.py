from rest_framework import serializers
from common.serializers import BaseModelSerializer
from .models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(BaseModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.CharField(write_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'product_id', 'quantity', 
                 'price', 'subtotal', 'created_at', 'updated_at')
        read_only_fields = ('order', 'price')

class OrderSerializer(BaseModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    items_data = OrderItemSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Order
        fields = ('id', 'user', 'total_amount', 'shipping_address', 
                 'status', 'payment_status', 'items', 'items_data',
                 'created_at', 'updated_at')
        read_only_fields = ('user', 'total_amount', 'status', 'payment_status')

    def create(self, validated_data):
        items_data = validated_data.pop('items_data', [])
        order = Order.objects.create(**validated_data)
        
        total_amount = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )
            total_amount += price * quantity
        
        order.total_amount = total_amount
        order.save()
        return order 