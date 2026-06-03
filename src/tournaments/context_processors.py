from .models import SiteSettings, Tournament


def site_settings(request):
    tournaments = Tournament.objects.filter(is_published=True)
    return {
        "site": SiteSettings.load(),
        "nav_tournaments": tournaments,
    }
