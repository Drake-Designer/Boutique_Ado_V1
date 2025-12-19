from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import OrderForm


def checkout(request):
    """Render the checkout page or redirect if bag is empty."""
    bag = request.session.get("bag", {})

    if not bag:
        messages.error(request, "There's nothing in your bag at the moment.")
        return redirect("products")

    order_form = OrderForm()

    context = {
        "order_form": order_form,
    }

    return render(request, "checkout/checkout.html", context)
