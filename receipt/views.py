from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Receipt, ReceiptItem
from receipt.serializer import ReceiptSerializer
from users.permissions import IsAdminOrIsCustomer, IsCustomer
from rest_framework import permissions
from users.permissions import IsAdminUser as IsAdmin
from rest_framework import status
from orders.models import Order, AdminNotification
# Create your views here.

class CreateReceiptView(APIView):
    permission_classes = [IsAdminOrIsCustomer]  

    def post(self, request):
        user = request.user
        try:
            order = Order.objects.filter(user=user).latest('order_date')  # Get the latest order
        except Order.DoesNotExist:
            return Response({"error": "No recent order found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not order.items.exists():
            return Response({"error": "Order is empty"}, status=status.HTTP_400_BAD_REQUEST)

        shipping_address = request.data.get('shipping_address')
        if not shipping_address:
            return Response({"error": "Shipping address is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create Receipt with status "Pending"
        receipt = Receipt.objects.create(
            user=user,
            receipt_amount=order.total_price,
            receipt_status="Pending",  # Not visible to customer
            receipt_created_by=request.user,
            receipt_created_date=order.order_date
        )

        for order_item in order.items.all():
            ReceiptItem.objects.create(
                receipt=receipt,
                product=order_item.product,
                quantity=order_item.quantity,
                price=order_item.price
            )

        # Change order status instead of deleting it
        order.status = "Processed"
        order.save()

        # Save notification for admin
        AdminNotification.objects.create(
            order=order,
            message=f"New order {order.id} placed by {user.username}. Needs review."
        )

        serializer = ReceiptSerializer(receipt)
        return Response({"message": "Receipt created successfully. Pending Admin Approval.", 'data': serializer.data}, status=status.HTTP_201_CREATED)

class ReceiptView(APIView):
    permission_classes = [IsAdminOrIsCustomer]

    def get(self, request):
        user = request.user
        receipts = Receipt.objects.filter(user=user)
        serializer = ReceiptSerializer(receipts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ApprovedReceiptView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        receipts = Receipt.objects.filter(is_approved=True)
        serializer = ReceiptSerializer(receipts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, receipt_id):
        try:
            receipt = Receipt.objects.get(id=receipt_id)
        except Receipt.DoesNotExist:
            return Response({"error": "Receipt not found"}, status=status.HTTP_404_NOT_FOUND)
        
        receipt.is_approved = True
        receipt.receipt_status = "Paid"
        receipt.save()

        return Response({"message": "Receipt approved successfully"}, status=status.HTTP_200_OK)