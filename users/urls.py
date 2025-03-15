from django.urls import path
from .views import RegisterationView, LoginView, AdminNotificationListView

urlpatterns = [
    path('register/', RegisterationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/Notifications/', AdminNotificationListView.as_view(), name='admin-notifications'),
]