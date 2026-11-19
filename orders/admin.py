from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "customer_phone",
        "product",
        "quantity",
        "total_price",
        "order_status",
        "created_at",
    )
    list_filter = ("order_status", "payment_method", "created_at")
    list_editable = ("order_status",)
    search_fields = ("customer_name", "customer_phone", "product__name")
    readonly_fields = ("created_at", "total_price")
