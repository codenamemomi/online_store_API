from django.db import models
from users.models import CustomUser as User
from products.models import Product
# Create your models here.


class Receipt(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'pending'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receipt_amount = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product, through='ReceiptItem', related_name='receipts')
    receipt_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    receipt_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_receipts')
    receipt_created_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        products_list = ", ".join([product.name for product in self.products.all()])
        return f"Receipt {self.id} - {self.user.email} - Total: {self.receipt_amount} - Status: {self.receipt_status} - Products: {products_list}"

class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        """ Automatically calculate the total before saving """
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.product.category}) - Receipt {self.receipt.id}"