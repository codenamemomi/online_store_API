from django.urls import path
from payments.views import CreatePaymentView, ExecutePaymentView, PaymentListView, PaymentDetailView

urlpatterns = [
    path('create/payment/', CreatePaymentView.as_view(), name='create-payment'),
    path('execute/payment/', ExecutePaymentView.as_view(), name='execute-payment'),
    path('payments/', PaymentListView.as_view(), name='payments'),
    path('payment/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
]