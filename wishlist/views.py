from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from products.models import Product
from .models import WishlistItem


@login_required
@require_POST
def toggle_wishlist(request, product_slug):
    """Add or remove a product from the user's wishlist."""
    product = get_object_or_404(Product, slug=product_slug)
    item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        item.delete()
        messages.info(request, f'"{product.name}" removed from your wishlist.')
    else:
        messages.success(request, f'"{product.name}" saved to your wishlist!')

    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    return redirect(next_url)


@login_required
def wishlist_page(request):
    """All saved products for the logged-in user."""
    items = WishlistItem.objects.filter(user=request.user).select_related("product")
    return render(request, "wishlist/wishlist.html", {"items": items})
