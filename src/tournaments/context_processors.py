from django.core.cache import cache

from .models import SiteBlock, SiteSettings
from .services import get_published_tournaments

SITE_BLOCKS_CACHE_KEY = "site_blocks_v1"
SITE_BLOCKS_CACHE_TTL = 60


def _load_site_blocks() -> dict[str, SiteBlock]:
    cached = cache.get(SITE_BLOCKS_CACHE_KEY)
    if cached is not None:
        return cached

    blocks = {block.cache_key: block for block in SiteBlock.objects.filter(is_active=True)}
    cache.set(SITE_BLOCKS_CACHE_KEY, blocks, SITE_BLOCKS_CACHE_TTL)
    return blocks


def site_settings(request):
    return {
        "site": SiteSettings.load(),
        "nav_tournaments": get_published_tournaments(),
        "site_blocks": _load_site_blocks(),
    }
