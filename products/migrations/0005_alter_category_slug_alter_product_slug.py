# Generated by Django 5.1.5 on 2025-01-18 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_category_slug_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
