from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """Configure the checkout app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "checkout"

    def ready(self) -> None:
        """Import signals when the app is ready."""
        import checkout.signals  # noqa: F401
