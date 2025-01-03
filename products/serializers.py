from rest_framework import serializers
from common.serializers import BaseModelSerializer
from .models import Category, Product

class CategorySerializer(BaseModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'parent', 'created_at', 'updated_at')

class ProductSerializer(BaseModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.CharField(write_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'price', 'stock',
                 'is_active', 'category', 'category_id', 'image',
                 'created_at', 'updated_at') 