from django.contrib import admin

from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """Show line items inside the order admin page."""

    model = OrderLineItem
    readonly_fields = ("lineitem_total",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Configure how orders are displayed in the admin."""

    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        "order_number",
        "date",
        "delivery_cost",
        "order_total",
        "grand_total",
    )

    fields = (
        "order_number",
        "date",
        "full_name",
        "email",
        "phone_number",
        "country",
        "postcode",
        "town_or_city",
        "street_address1",
        "street_address2",
        "county",
        "delivery_cost",
        "order_total",
        "grand_total",
    )

    list_display = (
        "order_number",
        "date",
        "full_name",
        "order_total",
        "delivery_cost",
        "grand_total",
    )

    ordering = ("-date",)
    search_fields = ("order_number", "full_name", "email")
    list_filter = ("date", "country")
