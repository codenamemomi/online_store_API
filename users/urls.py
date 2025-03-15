from django.urls import path
from .views import RegisterationView, LoginView, AdminNotificationView, LogoutView

urlpatterns = [
    path('register/', RegisterationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/Notifications/', AdminNotificationView.as_view(), name='admin'),
    path('logout/', LogoutView.as_view(), name='logout')
]