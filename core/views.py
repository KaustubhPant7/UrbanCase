from django.shortcuts import render
from products.models import Product, Category
from .models import Banner


def home(request):
    banners = Banner.objects.filter(is_active=True)
    featured_products = Product.objects.filter(
        is_available=True, is_featured=True
    ).select_related("category")[:8]
    categories = Category.objects.all()

    wishlist_ids = set()
    if request.user.is_authenticated:
        from wishlist.models import WishlistItem
        wishlist_ids = set(
            WishlistItem.objects.filter(user=request.user).values_list(
                "product_id", flat=True
            )
        )

    context = {
        "banners": banners,
        "featured_products": featured_products,
        "categories": categories,
        "user_wishlist_products": wishlist_ids,
    }
    return render(request, "core/home.html", context)
