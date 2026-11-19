from .models import SiteSettings, SiteLogo


def social_links(request):
    """
    Makes `social` (legacy) and `site_settings` available in every template.
    `social` is kept for backwards compatibility with any existing templates.
    Also exposes `site_logo` — the active uploaded logo (or None).
    """
    settings_obj = SiteSettings.objects.first()
    logo = SiteLogo.objects.filter(is_active=True).first()
    return {
        "social": settings_obj,          # legacy alias
        "site_settings": settings_obj,   # new name used by contact section
        "site_logo": logo,               # active logo for navbar
    }
