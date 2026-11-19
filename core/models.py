from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to="banners/")
    button_text = models.CharField(max_length=60, blank=True, default="Shop Now")
    button_link = models.CharField(max_length=200, blank=True, default="/products/")
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """Single-row model that stores contact info and social links shown site-wide."""

    # Contact details
    address = models.CharField(max_length=300, blank=True, help_text="Street / area, city, pincode")
    phone = models.CharField(max_length=30, blank=True, help_text="Display phone number, e.g. +91 98765 43210")
    email = models.EmailField(blank=True, help_text="Support / contact email")
    business_hours = models.CharField(
        max_length=200,
        blank=True,
        help_text="e.g. Mon – Sat: 9 AM – 7 PM | Sunday: Closed",
    )

    # Social links
    instagram_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="Include country code, e.g. 919876543210",
    )
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True, help_text="Twitter / X profile URL")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    @property
    def whatsapp_url(self):
        if self.whatsapp_number:
            return f"https://wa.me/{self.whatsapp_number}"
        return ""


# Keep old name as an alias so any existing references don't break
SocialLink = SiteSettings


class SiteLogo(models.Model):
    """Single-row model — upload your logo from the admin panel."""

    image = models.ImageField(
        upload_to="logos/",
        help_text="Recommended: transparent PNG or SVG-exported PNG, min 200 px tall.",
    )
    alt_text = models.CharField(
        max_length=120,
        default="UrbanCase",
        help_text="Alt text shown to screen readers and if the image fails to load.",
    )
    height = models.PositiveSmallIntegerField(
        default=40,
        help_text="Display height in pixels (width scales automatically).",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to fall back to the text logo.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Logo"
        verbose_name_plural = "Site Logo"

    def __str__(self):
        return f"Logo — {self.image.name}"
