from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from common.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'price', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'price', 'name']
    ordering = ['-created_at']

    @swagger_auto_schema(
        operation_summary="Get trending products",
        manual_parameters=[
            openapi.Parameter(
                'days',
                openapi.IN_QUERY,
                description="Number of days to consider for trending (default: 7)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Number of trending products to return (default: 10)",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={200: ProductSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def trending(self, request):
        days = int(request.query_params.get('days', 7))
        limit = int(request.query_params.get('limit', 10))
        
        # Get products ordered in the last X days
        since_date = timezone.now() - timedelta(days=days)
        trending_products = Product.objects.filter(
            is_active=True,
            orderitem__order__created_at__gte=since_date
        ).annotate(
            order_count=Count('orderitem')
        ).order_by('-order_count')[:limit]

        page = self.paginate_queryset(trending_products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(trending_products, many=True)
        return Response(serializer.data)
