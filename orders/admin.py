from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_id', 'total_price', 'status', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('user', 'order_id')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'id')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)