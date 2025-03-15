from rest_framework.views import APIView
from .serializers import UserSerializer
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
# Create your views here.

class RegisterationView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response('user registration page', status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('user registration successful', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None or password is None:
            return Response({'error': 'Please input both email and password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(email=email, password=password)
        
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
        
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        response = Response({
            'message': f"{user} logged in successfully",
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


class AdminNotificationView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        notifications = AdminNotification.objects.filter(created_at__gte=now()-timedelta(days=7))
        serializer = AdminNotificationSerializer(notifications, many=True)
        if not notifications.exists():
            return Response('No notifications', status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response = Response('Logout successful', status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response