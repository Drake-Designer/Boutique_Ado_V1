from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product


def view_bag(request):
    """Display the shopping bag contents."""
    return render(request, "bag/bag.html")


@require_POST
def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the bag."""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get("quantity", 1))
    redirect_url = request.POST.get("redirect_url") or "view_bag"

    bag = request.session.get("bag", {})
    item_id_str = str(item_id)

    bag[item_id_str] = bag.get(item_id_str, 0) + quantity
    request.session["bag"] = bag

    messages.success(request, f"Added {product.name} to your bag.")
    return redirect(redirect_url)


@require_POST
def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product in the bag."""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get("quantity", 1))

    bag = request.session.get("bag", {})
    item_id_str = str(item_id)

    if quantity > 0:
        bag[item_id_str] = quantity
        messages.success(request, f"Updated {product.name} quantity.")
    else:
        bag.pop(item_id_str, None)
        messages.success(request, f"Removed {product.name} from your bag.")

    request.session["bag"] = bag
    return redirect("view_bag")


@require_POST
def remove_from_bag(request, item_id):
    """Remove the specified product from the bag."""
    product = get_object_or_404(Product, pk=item_id)

    bag = request.session.get("bag", {})
    item_id_str = str(item_id)

    bag.pop(item_id_str, None)
    request.session["bag"] = bag

    messages.success(request, f"Removed {product.name} from your bag.")
    return redirect("view_bag")
