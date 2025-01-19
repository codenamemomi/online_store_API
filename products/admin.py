from django.contrib import admin
from .models import Product, Category


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'category', 'is_available', 'id')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'category__name')
    prepopulated_fields = {'slug': ('name',)}




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'id')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}