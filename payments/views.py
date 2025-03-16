from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema
from .models import Payment
from .serializers import PaymentSerializer
from orders.models import Order
from orders.serializers import OrderSerializer
from users.authentication import CookieJWTAuthentication
from users.permissions import IsAdminOrIsCustomer, IsAdminUser, IsCustomer
import paypalrestsdk
import os

# Create your views here.

paypalrestsdk.configure({
    'mode': os.getenv('PAYPAL_MODE'),
    'client_id': os.getenv('PAYPAL_CLIENT_ID'),
    'client_secret': os.getenv('PAYPAL_CLIENT_SECRET')
})

@extend_schema(tags=['Payments'])
class CreatePaymentView(GenericAPIView):
    permission_classes = [IsAdminOrIsCustomer]
    serializer_class = OrderSerializer

    @extend_schema(operation_id='create_payment')
    def post(self, request):
        user = request.user
        order_id = request.data.get('order_id')

        try:
            order = Order.objects.get(order_id=order_id, user=user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": str(order.total_price),
                    "currency": "USD"
                },
                "description": f"Order {order.order_id}"
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8009/store/execute/payment/",
                "cancel_url": "http://localhost:8009/store/cancle/payment/"
            }
        })

        if payment.create():
            payment_record = Payment.objects.create(
                user=user,
                order=order,
                paypal_payment_id=payment.id,
                amount=order.total_price,
                payment_status=payment.state,
            )
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return Response({"approval_url": approval_url}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)
        
@extend_schema(tags=['Payments'])
class ExecutePaymentView(GenericAPIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAdminOrIsCustomer]
    serializer_class = PaymentSerializer
    
    @extend_schema(operation_id='execute_payment')
    def get(self, request):
        payment_id = request.query_params.get('paymentId')
        payer_id = request.query_params.get('PayerID')
        
        payment = paypalrestsdk.Payment.find(payment_id)
        
        if payment.execute({"payer_id": payer_id}):
            payment_record = Payment.objects.get(paypal_payment_id=payment.id)
            payment_record.payment_status = payment.state
            payment_record.save()
            return Response({"message": "Payment executed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Payments'])
class PaymentListView(GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PaymentSerializer
    
    @extend_schema(operation_id='payment_list')
    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=['Payments'])
class PaymentDetailView(GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PaymentSerializer
    
    @extend_schema(operation_id='payment_detail')
    def get(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(operation_id='delete_payment')
    def delete(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        payment.delete()
        return Response({"message": "Payment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)