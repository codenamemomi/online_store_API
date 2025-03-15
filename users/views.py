from rest_framework.views import APIView
from .serializers import UserSerializer
from django.shortcuts import render
from rest_framework import permissions
from rest_framework_simplejwt.tokens import AccessToken
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
    

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None or password is None:
            return Response('Please input both email and password', status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(email=email, password=password)
        
        if user is None:
            return Response('Invalid credentials', status=status.HTTP_404_NOT_FOUND)
        
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    

class AdminNotificationListView(generics.ListAPIView):
    """ Retrieve admin notifications and mark them as viewed. """
    permission_classes = [IsAdmin]
    serializer_class = AdminNotificationSerializer

    def get_queryset(self):
        return AdminNotification.objects.filter(admin=self.request.user).order_by("-created_at")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        for notification in queryset:
            if not notification.viewed_at:
                notification.viewed_at = now()
                notification.save()

        print("Viewed notifications:", queryset.filter(viewed_at__isnull=False))

        five_minutes_ago = now() - timedelta(minutes=5)
        deleted_count, _ = AdminNotification.objects.filter(viewed_at__lte=five_minutes_ago).delete()

        print(f"Deleted {deleted_count} notifications")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
