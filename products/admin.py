from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for product categories.
    """

    list_display = (
        "name",
        "friendly_name",
    )
    ordering = ("name",)
    search_fields = ("name", "friendly_name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for products.
    """

    list_display = (
        "name",
        "sku",
        "category",
        "price",
        "rating",
        "is_active",
    )
    list_filter = (
        "category",
        "is_active",
    )
    search_fields = (
        "name",
        "sku",
        "description",
    )
    ordering = ("name",)

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "sku",
                    "category",
                    "description",
                )
            },
        ),
        (
            "Pricing & Rating",
            {
                "fields": (
                    "price",
                    "rating",
                )
            },
        ),
        (
            "Images",
            {
                "fields": (
                    "image",
                    "image_url",
                )
            },
        ),
        (
            "Status & Metadata",
            {
                "fields": (
                    "is_active",
                )
            },
        ),
    )
