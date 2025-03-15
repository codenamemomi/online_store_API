from rest_framework import serializers
from .models import Receipt, ReceiptItem
from products.models import Product
from users.models import CustomUser

class ReceiptItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ReceiptItem
        fields = ('product', 'quantity', 'price', 'total')

class ReceiptSerializer(serializers.ModelSerializer):
    items = ReceiptItemSerializer(many=True, read_only=True) 
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Receipt
        fields = ('id', 'user', 'receipt_created_date', 'receipt_status', 'is_approved', 'items')