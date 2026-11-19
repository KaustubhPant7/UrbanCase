from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("place/<slug:product_slug>/", views.place_order, name="place"),
    path("confirmation/<int:pk>/", views.order_confirmation, name="confirmation"),
    path("my-orders/", views.my_orders, name="my_orders"),
]
