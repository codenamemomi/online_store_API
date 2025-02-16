from django.contrib import admin
from .models import Receipt, ReceiptItem

# Register your models here.

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'receipt_amount', 'receipt_status', 'receipt_created_by', 'receipt_created_date')
    list_filter = ('receipt_status', 'receipt_created_date')
    search_fields = ('user', 'id')

class ReceiptItemAdmin(admin.ModelAdmin):
    list_display = ('receipt', 'product', 'quantity', 'price', 'total')

admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(ReceiptItem, ReceiptItemAdmin)
