# Generated by Django 5.1.5 on 2025-02-21 00:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_adminnotification_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminnotification',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='adminnotification',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
