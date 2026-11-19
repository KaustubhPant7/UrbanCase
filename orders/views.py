from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from products.models import Product
from .models import Order
from .forms import OrderForm


def place_order(request, product_slug):
    """COD order form for a specific product."""
    product = get_object_or_404(Product, slug=product_slug, is_available=True)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]

            if product.stock < quantity:
                if product.stock == 0:
                    form.add_error("quantity", "Sorry, this product is out of stock.")
                else:
                    form.add_error(
                        "quantity",
                        "Only {} unit(s) available.".format(product.stock),
                    )
            else:
                order = form.save(commit=False)
                order.product = product
                order.user = request.user if request.user.is_authenticated else None
                order.save()

                product.stock -= quantity
                product.save(update_fields=["stock"])

                request.session["order_confirmed_{}".format(order.pk)] = True

                messages.success(
                    request,
                    "Your order has been placed! We will contact you shortly.",
                )
                return redirect("orders:confirmation", pk=order.pk)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial["customer_name"] = (
                request.user.get_full_name() or request.user.email
            )
        form = OrderForm(initial=initial)

    context = {"product": product, "form": form}
    return render(request, "orders/place_order.html", context)


def order_confirmation(request, pk):
    """Thank-you page - only visible to the order owner or staff."""
    order = get_object_or_404(Order, pk=pk)

    if request.user.is_authenticated:
        if not request.user.is_staff and order.user != request.user:
            raise Http404
    elif order.user is not None:
        session_key = "order_confirmed_{}".format(pk)
        if not request.session.get(session_key):
            raise Http404

    return render(request, "orders/confirmation.html", {"order": order})


def my_orders(request):
    """Order history for logged-in users."""
    if not request.user.is_authenticated:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())

    orders = (
        Order.objects.filter(user=request.user)
        .select_related("product")
        .order_by("-created_at")
    )
    return render(request, "orders/my_orders.html", {"orders": orders})