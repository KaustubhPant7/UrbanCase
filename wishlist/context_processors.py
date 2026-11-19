from .models import WishlistItem


def wishlist_count(request):
    """Injects wishlist_count into every template."""
    if request.user.is_authenticated:
        count = WishlistItem.objects.filter(user=request.user).count()
    else:
        count = 0
    return {"wishlist_count": count}
