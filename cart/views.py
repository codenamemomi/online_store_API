from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .models import Cart, CartItem, Product
from .serializers import CartSerializer, CartItemSerializer
from products.serializers import productSerializer
from users.permissions import IsAdminOrIsCustomer
from users.permissions import IsAdminUser
from rest_framework import status
from drf_spectacular.utils import extend_schema

# Create your views here.
@extend_schema(tags=['Cart'])
class AddToCartView(GenericAPIView):
    permission_classes = [IsAdminOrIsCustomer]
    serializer_class = CartSerializer 

    @extend_schema(operation_id='add_to_cart')
    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(user=user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            new_quantity = cart_item.quantity + int(quantity)
            if new_quantity <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = new_quantity
                cart_item.save()
        else:
            if int(quantity) > 0:
                cart_item.quantity = int(quantity)
                cart_item.save()
            else:
                return Response({"error": "Quantity must be greater than zero for new items"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(cart)  # ✅ Use `self.get_serializer`
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(tags=['Cart'])
class CartView(GenericAPIView):
    permission_classes = [IsAdminOrIsCustomer]
    serializer_class = CartSerializer  # Default serializer

    def get_serializer_class(self):
        return CartSerializer  # Ensures all methods use the same serializer

    @extend_schema(operation_id='view_cart')
    def get(self, request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(cart)  # Uses the serializer dynamically
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(operation_id='modify_cart')
    def patch(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if product_id is None or quantity is None:
            return Response({"error": "Product ID and quantity are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
        except ValueError:
            return Response({"error": "Quantity must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        cart.calculate_total_price()
        serializer = self.get_serializer(cart)
        return Response({"message": "Items in cart have been modified", "data": serializer.data}, status=status.HTTP_200_OK)

    @extend_schema(operation_id='delete_cart_item')
    def delete(self, request):
        user = request.user
        product_id = request.data.get("product_id")

        if product_id is None:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        cart.calculate_total_price()
        serializer = self.get_serializer(cart)
        return Response({"message": "Item has been removed from cart", "data": serializer.data}, status=status.HTTP_200_OK)
