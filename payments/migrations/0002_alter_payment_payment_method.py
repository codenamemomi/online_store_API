# Generated by Django 5.1.5 on 2025-02-20 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(default='CARD', max_length=255),
        ),
    ]
