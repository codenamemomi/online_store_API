from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import productSerializer, categorySerializer
from users.permissions import IsAdminUser as IsAdmin
from users.permissions import IsCustomer, IsAdminOrIsCustomer
from drf_spectacular.utils import extend_schema

# Create your views here.
@extend_schema(tags=['Products'])
class ProductList(GenericAPIView):
    serializer_class = productSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAdminOrIsCustomer]
        else:
            self.permission_classes = [IsAdmin]
        return super(ProductList, self).get_permissions()

    @extend_schema(operation_id='product_list')
    def get(self, request):
        products = Product.objects.all()
        serializer = productSerializer(products, many=True)
        return Response({'message': 'products in stock', 'data': serializer.data}, status=status.HTTP_200_OK)

    @extend_schema(operation_id='add_product')
    def post(self, request):
        serializer = productSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'poduct has been added to stock', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Products'])
class ProductDetail(GenericAPIView):
    serializer_class = productSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAdminOrIsCustomer]
        else:
            self.permission_classes = [IsAdmin]
        return super(ProductDetail, self).get_permissions()

    @extend_schema(operation_id='product_detail')
    def get(self, request, id):
        product = Product.objects.get(id=id)
        serializer = productSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(operation_id='edit_product')
    def patch(self, request, id):
        product = Product.objects.get(id=id)
        serializer = productSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'producted has been updated', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(operation_id='delete_product')
    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response({'message': 'Product has been deleted'}, status=status.HTTP_204_NO_CONTENT)

@extend_schema(tags=['Categories'])
class CategoryList(GenericAPIView):
    serializer_class = categorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAdminOrIsCustomer]
        else:
            self.permission_classes = [IsAdmin]
        return super(CategoryList, self).get_permissions()

    @extend_schema(operation_id='category_list')
    def get(self, request):
        categories = Category.objects.all()
        serializer = categorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(operation_id='category_create')
    def post(self, request):
        serializer = categorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'category has been added', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Categories'])
class CategoryDetail(GenericAPIView):
    serializer_class = categorySerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            return [IsAdmin()]
        return [IsAdminOrIsCustomer()]

    @extend_schema(operation_id='category_detail')
    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = categorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(operation_id='create_category')
    def post(self, request):
        serializer = categorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'category has been added created', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(operation_id='edit_category')
    def patch(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = categorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(operation_id='delete_category')
    def delete(self, request, id):
        try:
            category = Category.objects.get(id=id)
            category.delete()
            return Response('category has been deleted', status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)