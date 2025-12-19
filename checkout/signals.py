from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_order_total_on_save(sender, instance, **kwargs):
    """Update order totals when a line item is saved."""
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    """Update order totals when a line item is deleted."""
    instance.order.update_total()
