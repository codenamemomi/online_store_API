from django.db import models
from orders.models import Order
from users.models import CustomUser

# Create your models here.

class Payment(models.Model):
    PAYMENT_CHOICES = (
        ('PAYPAL', 'Paypal'),
        ('CASH', 'Cash'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    paypal_payment_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=255, default='Pending')
    payment_method = models.CharField(max_length=255, default='paypal', choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.order_id} - Status: {self.payment_status}"
    

