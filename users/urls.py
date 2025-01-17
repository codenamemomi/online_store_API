from django.urls import path
from .views import RegisterationView, LoginView, AdminOnlyView

urlpatterns = [
    path('register/', RegisterationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/', AdminOnlyView.as_view(), name='admin'),
]