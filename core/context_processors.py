from .models import SiteSettings, SiteLogo


def site_context(request):
    """
    Injects site_settings and site_logo into every template context.
    Renamed from social_links; legacy alias kept for existing templates.
    Uses .first() with no repeated queries -- results are cached by Django ORM
    for the duration of the request.
    """
    settings_obj = SiteSettings.objects.first()
    logo = SiteLogo.objects.filter(is_active=True).first()
    return {
        "social": settings_obj,        # legacy alias used in product_detail.html
        "site_settings": settings_obj,
        "site_logo": logo,
    }
