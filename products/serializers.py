from rest_framework import serializers
from .models import Product, Category


class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','description', 'price', 'stock_quantity', 'category', 'image', 'updated_at', 'is_available')


class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'description')

