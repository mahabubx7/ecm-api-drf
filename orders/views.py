from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from cart.models import Cart

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Create order from cart",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'shipping_address': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['shipping_address']
        ),
        responses={201: OrderSerializer}
    )
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart = request.user.cart
        if not cart or not cart.items.exists():
            return Response(
                {'error': 'Cart is empty'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        shipping_address = request.data.get('shipping_address')
        if not shipping_address:
            return Response(
                {'error': 'Shipping address is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create order
        total_amount = sum(
            item.product.price * item.quantity 
            for item in cart.items.all()
        )
        
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            total_amount=total_amount
        )

        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Clear cart
        cart.items.all().delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Cancel order",
        responses={200: OrderSerializer}
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status != 'PENDING':
            return Response(
                {'error': 'Only pending orders can be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'CANCELLED'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
