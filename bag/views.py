from __future__ import annotations

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from products.models import Product


def view_bag(request):
    """Render the shopping bag page."""
    return render(request, "bag/bag.html")


def _safe_int(value, default: int = 1) -> int:
    """Convert a value to int safely."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _clamp_quantity(quantity: int, minimum: int = 1, maximum: int = 99) -> int:
    """Keep quantity within allowed limits."""
    return max(minimum, min(maximum, quantity))


def _get_bag(request) -> dict:
    """Return the bag session dict."""
    bag = request.session.get("bag", {})
    if not isinstance(bag, dict):
        bag = {}
    return bag


def _save_bag(request, bag: dict) -> None:
    """Save the bag back to the session."""
    request.session["bag"] = bag


@require_POST
def add_to_bag(request, item_id: int):
    """Add a quantity of the specified product to the shopping bag."""
    product = get_object_or_404(Product, pk=item_id)

    quantity = _clamp_quantity(
        _safe_int(request.POST.get("quantity"), default=1))
    redirect_url = request.POST.get("redirect_url") or reverse("products")
    size = request.POST.get("product_size")

    bag = _get_bag(request)
    item_id_str = str(item_id)

    if size:
        bag.setdefault(item_id_str, {"items_by_size": {}})
        bag[item_id_str].setdefault("items_by_size", {})

        bag[item_id_str]["items_by_size"][size] = (
            bag[item_id_str]["items_by_size"].get(size, 0) + quantity
        )

        messages.success(
            request,
            f"Added size {size.upper()} {product.name} to your bag",
            extra_tags="bag",
        )
    else:
        bag[item_id_str] = bag.get(item_id_str, 0) + quantity
        messages.success(
            request,
            f"Added {product.name} to your bag",
            extra_tags="bag",
        )

    _save_bag(request, bag)
    return redirect(redirect_url)


@require_POST
def update_bag(request, item_id: int):
    """Update the quantity for the specified product in the shopping bag."""
    product = get_object_or_404(Product, pk=item_id)

    quantity = _clamp_quantity(
        _safe_int(request.POST.get("quantity"), default=1))
    size = request.POST.get("product_size")

    bag = _get_bag(request)
    item_id_str = str(item_id)

    if item_id_str not in bag:
        messages.error(request, "That item is not in your bag.")
        return redirect(reverse("view_bag"))

    if size:
        item_data = bag.get(item_id_str, {})
        items_by_size = item_data.get("items_by_size", {})

        if not isinstance(items_by_size, dict):
            items_by_size = {}

        items_by_size[size] = quantity
        bag[item_id_str] = {"items_by_size": items_by_size}
    else:
        bag[item_id_str] = quantity

    _save_bag(request, bag)

    messages.success(
        request,
        f"Updated {product.name} quantity in your bag",
        extra_tags="bag",
    )
    return redirect(reverse("view_bag"))


@require_POST
def remove_from_bag(request, item_id: int):
    """Remove an item (or a size variant) from the shopping bag."""
    product = get_object_or_404(Product, pk=item_id)

    size = request.POST.get("product_size")
    bag = _get_bag(request)
    item_id_str = str(item_id)

    if item_id_str not in bag:
        return JsonResponse({"ok": False, "error": "Item not found in bag."}, status=404)

    if size:
        item_data = bag.get(item_id_str, {})
        items_by_size = item_data.get("items_by_size", {})

        if not isinstance(items_by_size, dict) or size not in items_by_size:
            return JsonResponse({"ok": False, "error": "Size not found in bag."}, status=404)

        items_by_size.pop(size, None)

        if items_by_size:
            bag[item_id_str] = {"items_by_size": items_by_size}
        else:
            bag.pop(item_id_str, None)
    else:
        bag.pop(item_id_str, None)

    _save_bag(request, bag)

    messages.success(
        request,
        f"Removed {product.name} from your bag",
        extra_tags="bag",
    )
    return JsonResponse({"ok": True}, status=200)
