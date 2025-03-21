from rest_framework import serializers
from .models import Product, Category


class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name','description', 'price', 'stock_quantity', 'category', 'image', 'updated_at', 'is_available')


class categorySerializer(serializers.ModelSerializer):
    products = productSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'products')

