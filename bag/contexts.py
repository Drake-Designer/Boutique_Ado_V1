from decimal import Decimal

from django.conf import settings
from django.shortcuts import get_object_or_404

from products.models import Product


def bag_contents(request):
    """Build the bag context from session data."""
    bag_items = []
    total = Decimal("0.00")
    product_count = 0

    bag = request.session.get("bag", {})

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)

        if isinstance(item_data, int):
            quantity = item_data
            total += quantity * product.price
            product_count += quantity

            bag_items.append(
                {
                    "item_id": item_id,
                    "quantity": quantity,
                    "product": product,
                    "subtotal": quantity * product.price,
                }
            )
        else:
            items_by_size = item_data.get("items_by_size", {})
            for size, quantity in items_by_size.items():
                total += quantity * product.price
                product_count += quantity

                bag_items.append(
                    {
                        "item_id": item_id,
                        "quantity": quantity,
                        "product": product,
                        "size": size,
                        "subtotal": quantity * product.price,
                    }
                )

    if total < Decimal(str(settings.FREE_DELIVERY_THRESHOLD)):
        delivery = total * \
            Decimal(str(settings.STANDARD_DELIVERY_PERCENTAGE)) / \
            Decimal("100")
        free_delivery_delta = Decimal(
            str(settings.FREE_DELIVERY_THRESHOLD)) - total
    else:
        delivery = Decimal("0.00")
        free_delivery_delta = Decimal("0.00")

    grand_total = total + delivery

    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        "grand_total": grand_total,
    }

    return context
