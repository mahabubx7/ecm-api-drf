from rest_framework import serializers
from django.contrib.auth import get_user_model
from common.serializers import BaseModelSerializer

User = get_user_model()

class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 
                 'phone', 'address', 'is_verified', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_verified') 