from rest_framework import serializers
from .models import Product, Category


class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
<<<<<<< HEAD
        fields = ('id','name','description', 'price', 'stock_quantity', 'category', 'image', 'updated_at', 'is_available')
=======
        fields = ('id', 'name','description', 'price', 'stock_quantity', 'category', 'image', 'updated_at', 'is_available')
>>>>>>> 50f05e1d4826d0bf25bedac2f3546483ee2234ca


class categorySerializer(serializers.ModelSerializer):
    products = productSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'products')

