from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order, InventoryItem, InventoryTransactionLog, LowStockAlert


@receiver(post_save, sender=Order)
def deduct_inventory_on_order(sender, instance, created, **kwargs):
    if not created and instance.status == Order.StatusChoices.PROCESSING:
        for item in instance.items.all():
            inventory = item.inventory_item
            if inventory and inventory.quantity_kg >= item.quantity_kg:
                inventory.quantity_kg -= item.quantity_kg
                inventory.save()

                InventoryTransactionLog.objects.create(
                    inventory_item=inventory,
                    action='order',
                    quantity_kg=item.quantity_kg,
                    performed_by=instance.user,
                    note=f"Auto-deducted by order #{instance.id}"
                )

                # Trigger low stock alert if needed
                if inventory.is_below_threshold() and not hasattr(inventory, 'low_stock_alert'):
                    LowStockAlert.objects.create(inventory_item=inventory)
