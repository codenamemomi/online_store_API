from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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

class CreatePaymentView(APIView):
    permission_classes = [IsAdminOrIsCustomer]

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
        

class ExecutePaymentView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAdminOrIsCustomer]
    
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
        
class PaymentListView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PaymentDetailView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        payment.delete()
        return Response({"message": "Payment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)