from decimal import Decimal

from django.conf import settings
from django.shortcuts import get_object_or_404

from products.models import Product


def bag_contents(request):
    """
    Build bag context data from the session.
    """
    bag_items = []
    total = Decimal("0.00")
    product_count = 0

    bag = request.session.get("bag", {})
    if not isinstance(bag, dict):
        bag = {}

    for item_id_str, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id_str)

        if isinstance(item_data, int):
            quantity = item_data
            subtotal = Decimal(quantity) * product.price

            total += subtotal
            product_count += quantity

            bag_items.append(
                {
                    "item_id": int(item_id_str),
                    "product": product,
                    "quantity": quantity,
                    "subtotal": subtotal,
                }
            )
            continue

        items_by_size = item_data.get("items_by_size", {})
        if not isinstance(items_by_size, dict):
            items_by_size = {}

        for size, quantity in items_by_size.items():
            subtotal = Decimal(quantity) * product.price

            total += subtotal
            product_count += quantity

            bag_items.append(
                {
                    "item_id": int(item_id_str),
                    "product": product,
                    "quantity": quantity,
                    "size": size,
                    "subtotal": subtotal,
                }
            )

    free_threshold = Decimal(
        str(getattr(settings, "FREE_DELIVERY_THRESHOLD", 0)))
    delivery_percentage = Decimal(
        str(getattr(settings, "STANDARD_DELIVERY_PERCENTAGE", 0)))

    if free_threshold and total < free_threshold:
        delivery = (total * delivery_percentage /
                    Decimal("100")).quantize(Decimal("0.01"))
        free_delivery_delta = (
            free_threshold - total).quantize(Decimal("0.01"))
    else:
        delivery = Decimal("0.00")
        free_delivery_delta = Decimal("0.00")

    grand_total = (total + delivery).quantize(Decimal("0.01"))

    context = {
        "bag_items": bag_items,
        "total": total.quantize(Decimal("0.01")),
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": free_threshold,
        "grand_total": grand_total,
    }

    return context
