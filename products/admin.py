from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ("image", "alt_text", "order")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "discount_price",
        "stock",
        "is_available",
        "is_featured",
    )
    list_filter = ("category", "is_available", "is_featured")
    list_editable = ("is_available", "is_featured", "stock")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "tagline", "description")
    readonly_fields = ("created_at", "updated_at")
    inlines = [ProductImageInline]
