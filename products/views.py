from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Category

PRODUCTS_PER_PAGE = 12


def _get_wishlist_products(user):
    """Return a set of product IDs in the user's wishlist."""
    if user.is_authenticated:
        from wishlist.models import WishlistItem
        return set(
            WishlistItem.objects.filter(user=user).values_list("product_id", flat=True)
        )
    return set()


def product_list(request):
    """All available products with optional category filter, search, sort, and pagination."""
    products = Product.objects.filter(is_available=True).select_related("category")
    categories = Category.objects.all()

    category_slug = request.GET.get("category", "").strip()
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "").strip()
    featured = request.GET.get("featured", "").strip()

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Use Q() so the category filter is not lost in a union
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if featured:
        products = products.filter(is_featured=True)

    if sort == "new":
        products = products.order_by("-created_at")
    elif sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")

    total_count = products.count()

    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    wishlist_ids = _get_wishlist_products(request.user)

    context = {
        "products": page_obj,
        "page_obj": page_obj,
        "total_count": total_count,
        "categories": categories,
        "selected_category": category,
        "query": query,
        "sort": sort,
        "featured": featured,
        "user_wishlist_products": wishlist_ids,
    }
    return render(request, "products/product_list.html", context)


def product_detail(request, slug):
    """Single product detail page."""
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(pk=product.pk)[:4]

    wishlist_ids = _get_wishlist_products(request.user)
    in_wishlist = product.pk in wishlist_ids
    gallery = product.gallery.all()

    context = {
        "product": product,
        "related_products": related,
        "in_wishlist": in_wishlist,
        "gallery": gallery,
    }
    return render(request, "products/product_detail.html", context)
