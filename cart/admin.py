from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'total_price', 'created_at', 'updated_at')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'id', 'product', 'quantity', 'price')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
