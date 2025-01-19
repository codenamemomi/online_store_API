from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    description = models.TextField()

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/')
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name