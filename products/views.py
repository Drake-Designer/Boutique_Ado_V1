from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Category, Product


def all_products(request):
    """
    Show all products with optional sorting, category filtering, and search.
    """
    products = Product.objects.select_related("category").all()

    search_term = None
    current_categories = None
    sort = None
    direction = None

    allowed_sorts = {"price", "rating", "name", "category"}
    allowed_directions = {"asc", "desc"}

    if request.GET:
        sort_param = request.GET.get("sort")
        direction_param = request.GET.get("direction")

        if sort_param in allowed_sorts:
            sort = sort_param
            sort_key = sort_param

            if sort_param == "name":
                sort_key = "lower_name"
                products = products.annotate(lower_name=Lower("name"))

            if sort_param == "category":
                sort_key = "category__name"

            if direction_param in allowed_directions:
                direction = direction_param

            if direction == "desc":
                sort_key = f"-{sort_key}"

            products = products.order_by(sort_key)

        category_param = request.GET.get("category")
        if category_param:
            category_names = [c.strip()
                              for c in category_param.split(",") if c.strip()]
            if category_names:
                products = products.filter(category__name__in=category_names)
                current_categories = Category.objects.filter(
                    name__in=category_names)

        q_param = request.GET.get("q")
        if q_param is not None:
            search_term = q_param.strip()
            if not search_term:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse("products"))

            queries = Q(name__icontains=search_term) | Q(
                description__icontains=search_term)
            products = products.filter(queries)

    current_sorting = f"{sort}_{direction}"

    context = {
        "products": products,
        "search_term": search_term,
        "current_categories": current_categories,
        "current_sorting": current_sorting,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """
    Show a single product detail page.
    """
    product = get_object_or_404(
        Product.objects.select_related("category"), pk=product_id)

    context = {
        "product": product,
    }

    return render(request, "products/product_detail.html", context)
