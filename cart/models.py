from django.db import models
from users.models import CustomUser
from products.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add= True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    products = models.ManyToManyField(Product, through='CartItem')
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"Cart {self.id} of user {self.user.last_name}"
    
    def calculate_total_price(self):
        total = sum(item.price * item.quantity for item in self.items.all())
        self.total_price = total
        self.save()
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantity} Item {self.product.name} item category {self.product.category} of cart {self.cart.id}"
    
    def save(self, *args, **extrafields):
        self.price = self.product.price
        super().save(*args, **extrafields)
        self.cart.calculate_total_price()