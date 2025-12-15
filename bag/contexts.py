from decimal import Decimal

from django.conf import settings

from products.models import Product


def bag_contents(request):
    """
    Build bag context data from session.
    """

    bag_items = []
    total = Decimal("0.00")
    product_count = 0
    bag = request.session.get("bag", {})

    for item_id, quantity in bag.items():
        try:
            product = Product.objects.get(pk=item_id)
        except Product.DoesNotExist:
            # Skip invalid product ids
            continue

        item_total = product.price * quantity
        total += item_total
        product_count += quantity

        bag_items.append(
            {
                "item_id": item_id,
                "product": product,
                "quantity": quantity,
                "item_total": item_total,
            }
        )

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * \
            Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / Decimal("100")
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
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
