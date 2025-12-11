from typing import Optional

from django.contrib import messages
from django.db.models import Q, QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Product, Category


def all_products(request):
    """
    View to show all products, with optional search, filtering and sorting.
    """
    products: QuerySet[Product] = Product.objects.all()

    query: Optional[str] = None
    categories_filter: Optional[list[str]] = None
    sort: Optional[str] = None
    direction: Optional[str] = None

    if request.GET:
        # Sorting
        if "sort" in request.GET:
            sort_key = request.GET.get("sort")
            sort = sort_key

            # Map sort options to model fields
            if sort_key == "name":
                sort_key = "name"
            elif sort_key == "price":
                sort_key = "price"
            elif sort_key == "rating":
                sort_key = "rating"
            elif sort_key == "category":
                sort_key = "category__name"

            if "direction" in request.GET:
                direction = request.GET.get("direction")
                if direction == "desc":
                    sort_key = f"-{sort_key}"

            if sort_key:
                products = products.order_by(sort_key)

        # Filter by category or categories (comma separated)
        if "category" in request.GET:
            categories_filter = request.GET.get("category", "").split(",")
            products = products.filter(category__name__in=categories_filter)
            categories_qs = Category.objects.filter(name__in=categories_filter)
        else:
            categories_qs = None

        # Search
        if "q" in request.GET:
            query = request.GET.get("q", "").strip()
            if not query:
                messages.error(
                    request, "You did not enter any search criteria.")
                return redirect(reverse("products"))

            search_queries = (
                Q(name__icontains=query)
                | Q(description__icontains=query)
            )
            products = products.filter(search_queries)

    current_sorting = f"{sort}_{direction}" if sort and direction else ""

    context = {
        "products": products,
        "search_term": query,
        "current_categories": categories_qs if "categories_qs" in locals() else None,
        "current_sorting": current_sorting,
    }
    return render(request, "products/products.html", context)


def product_detail(request, product_id: int):
    """
    View to show a single product detail.
    """
    product = get_object_or_404(Product, pk=product_id)

    context = {
        "product": product,
    }
    return render(request, "products/product_detail.html", context)
