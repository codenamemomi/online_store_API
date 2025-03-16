from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, LoginSerializer
from django.shortcuts import render
from rest_framework import permissions
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import permissions
from .permissions import IsAdminUser as IsAdmin
from rest_framework import generics, status
from orders.models import AdminNotification
from orders.serializers import AdminNotificationSerializer
from django.utils.timezone import now
from datetime import timedelta
from orders.models import AdminNotification
from drf_spectacular.utils import extend_schema
# Create your views here.

@extend_schema(tags=['Auth'])
class RegisterationView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    @extend_schema(operation_id='register_user')
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('user registration successful', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Auth'])
class LoginView(GenericAPIView):  # Changed from APIView to GenericAPIView
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer  # Added this line for Swagger support

    @extend_schema(operation_id='login_user')
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validates email & password

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(email=email, password=password)
        
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
        
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        response = Response({
            'message': f"{user} login successful",
            'access_token': str(access_token),
            'refresh_token': str(refresh_token),
        }, status=status.HTTP_200_OK)  

        response.set_cookie(
            key='access_token',
            value=str(access_token),
            httponly=True,
            samesite='None',  
            secure=True  
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh_token),
            httponly=True,
            samesite='None',
            secure=True
        )
        return response  


@extend_schema(tags=['Notifications'])
class AdminNotificationView(GenericAPIView):
    permission_classes = [IsAdmin]
    serializer_class = AdminNotificationSerializer
    
    @extend_schema(operation_id='get_notifications')
    def get(self, request):
        notifications = AdminNotification.objects.filter(created_at__gte=now()-timedelta(days=7))
        serializer = AdminNotificationSerializer(notifications, many=True)
        if not notifications.exists():
            return Response('No notifications', status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

 
@extend_schema(tags=['Auth'])
class LogoutView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoginSerializer

    @extend_schema(operation_id='logout_user')
    def post(self, request):
        response = Response('Logout successful', status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response