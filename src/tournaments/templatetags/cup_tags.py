from django import template
from django.utils.safestring import mark_safe

from src.tournaments.block_defaults import BLOCK_DEFAULTS
from src.tournaments.utils.site_block_text import get_plain_block_text
from src.tournaments.utils.block_placeholders import apply_block_placeholders
from src.tournaments.utils.block_render import render_block_html
from src.tournaments.utils.html import sanitize_html

register = template.Library()


@register.filter
def split(value: str, arg: str = " ") -> list:
    return value.split(arg)


@register.filter
def pad02(value: int) -> str:
    return str(value).zfill(2)


@register.filter
def safe_html(value: str) -> str:
    return mark_safe(sanitize_html(value))


@register.simple_tag
def block_plain(page: str, key: str, fallback: str = "") -> str:
    return get_plain_block_text(page, key, fallback=fallback)


@register.simple_tag(takes_context=True)
def render_block(context, page: str, key: str, fallback: str = "") -> str:
    blocks = context.get("site_blocks", {})
    block = blocks.get(f"{page}.{key}")
    rendered = render_block_html(block)
    if rendered:
        return rendered

    default = fallback or BLOCK_DEFAULTS.get((page, key), "")
    default = apply_block_placeholders(default)
    return mark_safe(sanitize_html(default) if default else "")
