# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import AdminNotification
# from orders.models import Order


# @receiver(post_save, sender=Order)
# def create_order_notification(sender, instance, created, **kwargs):
#     if created:
#         AdminNotification.objects.create(
#             order=instance,
#             message=f"New order placed by {instance.user}. Order ID: {instance.order_id}"
#         )
