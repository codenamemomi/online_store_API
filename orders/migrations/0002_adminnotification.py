<<<<<<< HEAD
# Generated by Django 5.1.5 on 2025-02-20 22:44

import django.db.models.deletion
from django.conf import settings
=======
# Generated by Django 5.1.5 on 2025-02-16 21:34

import django.db.models.deletion
>>>>>>> 50f05e1d4826d0bf25bedac2f3546483ee2234ca
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
<<<<<<< HEAD
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
=======
>>>>>>> 50f05e1d4826d0bf25bedac2f3546483ee2234ca
    ]

    operations = [
        migrations.CreateModel(
            name='AdminNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
<<<<<<< HEAD
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('viewed_at', models.DateTimeField(blank=True, null=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
=======
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='orders.order')),
>>>>>>> 50f05e1d4826d0bf25bedac2f3546483ee2234ca
            ],
        ),
    ]
