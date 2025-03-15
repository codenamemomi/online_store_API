from django.db import models
from users.models import CustomUser
from products.models import Product
from django.utils.timezone import now
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255, default='Pending')
    shipping_address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} of user {self.user.last_name} Total Price: {self.total_price}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantity} Item {self.product.name} item category {self.product.category} of order {self.order.order_id}"
    

class AdminNotification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f"Notification for Order {self.order.id} by user: {self.order.user.email} - {self.created_at}"
