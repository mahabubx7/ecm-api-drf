from django.shortcuts import render
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_summary="Register new user",
        request_body=RegisterSerializer,
        responses={201: RegisterSerializer}
    )
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Login user",
        request_body=LoginSerializer,
        responses={200: 'Token pair'}
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={201: RegisterSerializer()},
    security=[]  # This indicates no security required for Swagger
)
@api_view(['POST'])
@permission_classes([AllowAny])  # Explicitly allow all
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    return Response({
        'user': serializer.data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={200: 'JWT Token'},
    security=[]  # This indicates no security required for Swagger
)
@api_view(['POST'])
@permission_classes([AllowAny])  # Explicitly allow all
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(**serializer.validated_data)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )
