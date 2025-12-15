from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("name",)

    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def get_friendly_name(self) -> str:
        return self.friendly_name or self.name


class Product(models.Model):
    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["category"]),
        ]

    category = models.ForeignKey(
        "Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    sku = models.CharField(max_length=254, null=True,
                           blank=True, db_index=True)
    name = models.CharField(max_length=254, db_index=True)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    @property
    def display_image_url(self) -> str:
        """
        Return a safe image URL for templates.
        """
        if self.image and getattr(self.image, "url", None):
            return self.image.url
        if self.image_url:
            return self.image_url
        return ""
