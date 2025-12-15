from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from products.models import Product


def view_bag(request):
    """
    Render the bag contents page.
    """
    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """
    Add a quantity of a product to the shopping bag.
    """
    product = get_object_or_404(Product, pk=item_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(1, min(99, quantity))

    redirect_url = request.POST.get("redirect_url") or reverse("products")
    size = request.POST.get("product_size")

    bag = request.session.get("bag", {})

    item_id_str = str(item_id)

    if size:
        bag.setdefault(item_id_str, {"items_by_size": {}})
        bag[item_id_str].setdefault("items_by_size", {})
        bag[item_id_str]["items_by_size"][size] = bag[item_id_str]["items_by_size"].get(
            size, 0) + quantity

        messages.success(
            request,
            f"Added {product.name} (size {size.upper()}) to your bag.",
        )
    else:
        bag[item_id_str] = bag.get(item_id_str, 0) + quantity
        messages.success(
            request,
            f"Added {product.name} to your bag.",
        )

    request.session["bag"] = bag
    return redirect(redirect_url)


def update_bag(request, item_id):
    """
    Update the quantity of a product in the shopping bag.
    """
    if request.method != "POST":
        return redirect(reverse("view_bag"))

    product = get_object_or_404(Product, pk=item_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(0, min(99, quantity))
    size = request.POST.get("product_size")

    bag = request.session.get("bag", {})
    item_id_str = str(item_id)

    if size:
        if item_id_str not in bag or "items_by_size" not in bag[item_id_str]:
            messages.error(request, "That item is not in your bag.")
            return redirect(reverse("view_bag"))

        if quantity > 0:
            bag[item_id_str]["items_by_size"][size] = quantity
            messages.success(
                request,
                f"Updated {product.name} (size {size.upper()}) quantity to {quantity}.",
            )
        else:
            bag[item_id_str]["items_by_size"].pop(size, None)
            messages.success(
                request,
                f"Removed {product.name} (size {size.upper()}) from your bag.",
            )

            if not bag[item_id_str]["items_by_size"]:
                bag.pop(item_id_str, None)
    else:
        if quantity > 0:
            bag[item_id_str] = quantity
            messages.success(
                request,
                f"Updated {product.name} quantity to {quantity}.",
            )
        else:
            bag.pop(item_id_str, None)
            messages.success(
                request,
                f"Removed {product.name} from your bag.",
            )

    request.session["bag"] = bag
    return redirect(reverse("view_bag"))


def remove_from_bag(request, item_id):
    """
    Remove a product from the shopping bag.
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method.")

    product = get_object_or_404(Product, pk=item_id)
    size = request.POST.get("size")

    bag = request.session.get("bag", {})
    item_id_str = str(item_id)

    try:
        if size:
            bag[item_id_str]["items_by_size"].pop(size, None)

            if not bag[item_id_str]["items_by_size"]:
                bag.pop(item_id_str, None)

            messages.success(
                request,
                f"Removed {product.name} (size {size.upper()}) from your bag.",
            )
        else:
            bag.pop(item_id_str, None)
            messages.success(
                request,
                f"Removed {product.name} from your bag.",
            )

        request.session["bag"] = bag
        return HttpResponse(status=200)
    except KeyError:
        return HttpResponseBadRequest("Item not found.")
