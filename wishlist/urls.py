from django.urls import path
from . import views

app_name = "wishlist"

urlpatterns = [
    path("", views.wishlist_page, name="list"),
    path("toggle/<slug:product_slug>/", views.toggle_wishlist, name="toggle"),
]
