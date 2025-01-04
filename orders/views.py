from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from cart.models import Cart
from rest_framework.permissions import AllowAny, IsAuthenticated

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        """
        Retrieve (order tracking) is public
        Other actions require authentication
        """
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        For authenticated users: return their orders
        For anonymous users: only allow access to specific order by ID
        """
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        # For anonymous users doing order tracking
        order_id = self.kwargs.get('pk')
        if order_id:
            return Order.objects.filter(id=order_id)
        return Order.objects.none()

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

    @swagger_auto_schema(
        operation_summary="Track order status",
        manual_parameters=[
            openapi.Parameter(
                'order_id',
                openapi.IN_QUERY,
                description="Order ID to track",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: OrderSerializer}
    )
    @action(detail=False, methods=['get'])
    def track_order(self, request):
        order_id = request.query_params.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
