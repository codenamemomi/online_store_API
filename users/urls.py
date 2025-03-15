from django.urls import path
<<<<<<< HEAD
from .views import RegisterationView, LoginView, AdminNotificationListView
=======
from .views import RegisterationView, LoginView, AdminNotificationView
>>>>>>> 50f05e1d4826d0bf25bedac2f3546483ee2234ca

urlpatterns = [
    path('register/', RegisterationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
<<<<<<< HEAD
    path('admin/Notifications/', AdminNotificationListView.as_view(), name='admin-notifications'),
=======
    path('admin/Notifications/', AdminNotificationView.as_view(), name='admin'),
>>>>>>> 50f05e1d4826d0bf25bedac2f3546483ee2234ca
]