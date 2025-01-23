from rest_framework import serializers
from .models import Payment
from orders.models import Order
from users.models import CustomUser


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'