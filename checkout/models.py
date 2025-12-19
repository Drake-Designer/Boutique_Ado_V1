import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from products.models import Product

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


class Order(models.Model):
    """Store an order and calculated totals."""

    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=Decimal("0.00"))
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=Decimal("0.00"))
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=Decimal("0.00"))

    if TYPE_CHECKING:
        lineitems: "RelatedManager[OrderLineItem]"

    def _generate_order_number(self) -> str:
        """Generate a unique order number."""
        return uuid.uuid4().hex.upper()

    def update_total(self) -> None:
        """Recalculate totals from line items and delivery rules."""
        total = self.lineitems.aggregate(
            total=Sum("lineitem_total")).get("total") or Decimal("0.00")
        total = Decimal(total).quantize(Decimal("0.01"))
        self.order_total = total

        threshold = Decimal(
            str(getattr(settings, "FREE_DELIVERY_THRESHOLD", 0)))
        percentage = Decimal(
            str(getattr(settings, "STANDARD_DELIVERY_PERCENTAGE", 0)))

        if self.order_total < threshold:
            self.delivery_cost = (
                self.order_total * percentage / Decimal("100")).quantize(Decimal("0.01"))
        else:
            self.delivery_cost = Decimal("0.00")

        self.grand_total = (self.order_total +
                            self.delivery_cost).quantize(Decimal("0.01"))
        self.save(update_fields=["order_total",
                  "delivery_cost", "grand_total"])

    def save(self, *args, **kwargs):
        """Set the order number if it is missing."""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return the order number."""
        return self.order_number


class OrderLineItem(models.Model):
    """Store a product line within an order."""

    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="lineitems",
    )
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)])
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """Calculate the line total and update the order."""
        self.lineitem_total = (self.product.price *
                               self.quantity).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)
        self.order.update_total()

    def __str__(self) -> str:
        """Return a readable line label."""
        sku = getattr(self.product, "sku", "")
        return f"SKU {sku} on order {self.order.order_number}"
