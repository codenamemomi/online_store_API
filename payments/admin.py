from django.contrib import admin
from .models import Payment

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'amount', 'payment_status')
    list_filter = ('payment_status', 'created_at')
    search_fields = ('user', 'id')

admin.site.register(Payment, PaymentAdmin)