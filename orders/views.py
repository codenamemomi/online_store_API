from django.shortcuts import render
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import timedelta
from rest_framework.views import APIView
from .models import Order, OrderItem, Product, AdminNotification, CustomUser
from .serializers import OrderSerializer, OrderItemSerializer
from users.permissions import IsAdminOrIsCustomer, IsCustomer
from users.permissions import IsAdminUser as IsAdmin
from rest_framework import status
from cart.models import Cart
from payments.models import Payment
# Create your views here.

class PlaceOrderView(APIView):
    permission_classes = [IsAdminOrIsCustomer]


    def post(self, request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        shipping_address = request.data.get('shipping_address')
        if not shipping_address:
            return Response({"error": "Shipping address is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(
            user=user,
            total_price=cart.total_price,
            status="Pending",
            shipping_address=shipping_address
        )

        for cart_item in cart.items.all():
            product = cart_item.product
           
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity,
                price=cart_item.price
            )
            
        cart.items.all().delete()
        cart.total_price = 0
        cart.save()

        serializer = OrderSerializer(order)
        return Response({"message": "Order placed successfully\nMove on to PAYMENT", 'data': serializer.data}, status=status.HTTP_201_CREATED)
    

class OrderView(APIView):
    permission_classes = [IsAdminOrIsCustomer]

    def get(self, request):
        user = request.user
        
        if user.is_staff:  # ✅ Admin can see all orders
            orders = Order.objects.all()
        else:  # ✅ Regular users see only their own orders
            orders = Order.objects.filter(user=user)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class OrderViewDetail(APIView):
    def get_permissions(self):
            if self.request.method in [ 'PATCH']:
                return [IsAdmin()]
            return [IsAdminOrIsCustomer()]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, order_id):

        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        current_status = order.status
        new_status = request.data.get('status')

        payment_made = Payment.objects.filter(order=order, payment_status= 'approved').exists()

        if current_status == "Pending" and not payment_made:
            return Response({"error": "Order status cannot be updated until payment is made"}, status=status.HTTP_400_BAD_REQUEST)

        if current_status == "pending" and new_status not in ["shipped", "delivered"]:
            return Response({"error": "Order status cannot be updated"}, status=status.HTTP_400_BAD_REQUEST)
        
        if current_status == "shipped" and new_status != "delivered":
            return Response({"error": "Order status cannot be updated"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order status updated successfully", 'data': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)