from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from . models import OrderItem


def update_on_save(sender, instance, created, **kwargs):
    order_items = instance.order.order_items.all()
    subtotal = sum(item.subtotal() for item in order_items)
    instance.order.order_total = subtotal
    instance.order.save()


@receiver(post_delete, sender=OrderItem)
def update_on_delete(sender, instance, **kwargs):

    instance.order.subtotal()
