from rest_framework import serializers
from .models import Order, OrderItem, AdminNotification
from products.models import Product
from users.models import CustomUser

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product= serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'order', 'id')

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    order_items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Order
        fields = ('order_id','user', 'total_price', 'status', 'shipping_address', 'order_items')

class AdminNotificationSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    admin = serializers.StringRelatedField()
    order = serializers.StringRelatedField()

    class Meta:
        model = AdminNotification
        fields = ('admin', 'order', 'message', 'created_at')