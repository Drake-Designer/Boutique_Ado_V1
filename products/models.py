from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    """
    Product category, used to group products in the catalog.
    """

    name = models.CharField(
        max_length=254,
        unique=True,
        help_text="Internal name used as identifier in code and fixtures.",
    )
    friendly_name = models.CharField(
        max_length=254,
        null=True,
        blank=True,
        help_text="Human readable name shown in the UI.",
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    def get_friendly_name(self) -> str:
        """
        Return a human friendly name and fall back to the internal one
        if a friendly name is not provided.
        """
        return self.friendly_name or self.name


class Product(models.Model):
    """
    Single product available in the store.
    """

    category = models.ForeignKey(
        "Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
        help_text="Category this product belongs to.",
    )
    sku = models.CharField(
        max_length=254,
        null=True,
        blank=True,
        db_index=True,
        help_text="Stock keeping unit or external product identifier.",
    )
    name = models.CharField(
        max_length=254,
        db_index=True,
        help_text="Product name shown in the catalog.",
    )
    description = models.TextField(
        help_text="Detailed description of the product.",
    )
    price = models.DecimalField(
        max_digits=7,          # up to 99999.99
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Price in EUR.",
    )
    rating = models.DecimalField(
        max_digits=3,          # 0.0 to 5.0
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Average customer rating, from 0.0 to 5.0.",
    )
    image_url = models.URLField(
        max_length=1024,
        null=True,
        blank=True,
        help_text="Legacy external image URL, kept for backward compatibility.",
    )
    image = models.ImageField(
        upload_to="products/",
        null=True,
        blank=True,
        help_text="Locally stored product image.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="If false, the product will be hidden from the catalog.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the product was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of the last update.",
    )

    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["sku"]),
        ]

    def __str__(self) -> str:
        return self.name
