from django.contrib import admin
from .models import Banner, SiteSettings, SiteLogo


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order")
    list_editable = ("is_active", "order")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("phone", "email", "updated_at")

    fieldsets = (
        ("Contact Information", {
            "fields": ("address", "phone", "email", "business_hours"),
        }),
        ("Social Links", {
            "fields": ("instagram_url", "whatsapp_number", "facebook_url", "twitter_url"),
        }),
    )

    def has_add_permission(self, request):
        # Only one row allowed
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteLogo)
class SiteLogoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_active", "height", "updated_at")
    list_editable = ("is_active",)
    readonly_fields = ("updated_at", "logo_preview")

    fieldsets = (
        (None, {
            "fields": ("image", "logo_preview", "alt_text", "height", "is_active"),
        }),
        ("Info", {
            "fields": ("updated_at",),
        }),
    )

    def logo_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html(
                '<img src="{}" height="{}" style="background:#111;padding:8px;border-radius:6px;" />',
                obj.image.url,
                min(obj.height * 2, 120),
            )
        return "—"
    logo_preview.short_description = "Preview"

    def has_add_permission(self, request):
        # Only one logo row allowed at a time
        return not SiteLogo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return True
