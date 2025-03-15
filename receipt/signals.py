from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Receipt, ReceiptItem
from orders.models import Order

@receiver(post_save, sender=Order)
def create_receipt(sender, instance, created, **kwargs):
    if created:
        order = instance
        user = order.user
        receipt = Receipt.objects.create(
            user=user,
            receipt_amount=order.total_price,
            receipt_status="Pending",
            receipt_created_by=user
        )

        for order_item in order.items.all():
            ReceiptItem.objects.create(
                receipt=receipt,
                product=order_item.product,
                quantity=order_item.quantity,
                price=order_item.price
            )