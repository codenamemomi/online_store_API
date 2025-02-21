from rest_framework import serializers
from .models import Payment
from orders.models import Order
from users.models import CustomUser


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    user = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ('user', 'order', 'amount', 'payment_method', 'payment_status',)