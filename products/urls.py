from django.urls import path
from .views import ProductList, CategoryList, ProductDetail, CategoryDetail

urlpatterns = [
    path('products/', ProductList.as_view(), name='product_list'),
    path('products/<int:id>/', ProductDetail.as_view(), name='product_detail'),
    path('categories/', CategoryList.as_view(), name='category_list'),
    path('categories/<int:id>/', CategoryDetail.as_view(), name='category_detail'),

    ]