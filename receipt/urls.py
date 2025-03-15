from django.urls import path
from .views import ApprovedReceiptView, ReceiptView

urlpatterns = [
    path('receipt/', ReceiptView.as_view(), name='receipt'),
    path('approve/', ApprovedReceiptView.as_view(), name='approve-receipt'),
    path('approve/<int:id>/', ApprovedReceiptView.as_view(), name='approve-receipt'),
]