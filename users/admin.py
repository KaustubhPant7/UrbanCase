from django.contrib import admin
from .models import EmailOTP


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ("email", "otp", "created_at", "expires_at", "attempts")
    readonly_fields = ("email", "otp", "password_hash", "created_at", "expires_at", "attempts")
    list_filter = ("created_at",)

    def has_add_permission(self, request):
        return False
