from rest_framework import serializers
from .models import CartItem , Cart


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    class Meta:
        model = CartItem
        fields = ('product', 'quantity', 'price', 'cart', 'id')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many = True, read_only= True)
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Cart
        fields = ('user', 'items', 'total_price')