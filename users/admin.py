from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import Group
from orders.models import AdminNotification

# Register your models here.



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'email', 'is_staff', 'is_active', 'role', 'id')
    search_fields = ('first_name', 'email')

class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at', 'order')
    search_fields = ('message', 'order')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)