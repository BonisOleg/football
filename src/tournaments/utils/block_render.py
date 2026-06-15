import re
from urllib.parse import parse_qs, urlparse

from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .block_placeholders import apply_block_placeholders
from .html import sanitize_html


def video_embed_html(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url.strip())
    host = (parsed.netloc or "").lower().replace("www.", "")

    if host in {"youtube.com", "youtu.be", "m.youtube.com"}:
        video_id = _youtube_id(url, parsed)
        if video_id:
            return format_html(
                '<div class="site-block-video">'
                '<iframe src="https://www.youtube.com/embed/{}" '
                'title="Video" loading="lazy" '
                'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
                'allowfullscreen></iframe></div>',
                video_id,
            )

    if host in {"vimeo.com", "player.vimeo.com"}:
        video_id = _vimeo_id(parsed)
        if video_id:
            return format_html(
                '<div class="site-block-video">'
                '<iframe src="https://player.vimeo.com/video/{}" '
                'title="Video" loading="lazy" allowfullscreen></iframe></div>',
                video_id,
            )

    return format_html(
        '<div class="site-block-video">'
        '<iframe src="{}" title="Video" loading="lazy" allowfullscreen></iframe></div>',
        url,
    )


def _youtube_id(url: str, parsed) -> str | None:
    host = (parsed.netloc or "").lower().replace("www.", "")
    if host == "youtu.be":
        return parsed.path.lstrip("/").split("/")[0] or None
    if "youtube.com" in host:
        if parsed.path == "/watch":
            ids = parse_qs(parsed.query).get("v", [])
            return ids[0] if ids else None
        match = re.match(r"^/(embed|shorts)/([^/?]+)", parsed.path)
        if match:
            return match.group(2)
    return None


def _vimeo_id(parsed) -> str | None:
    match = re.match(r"^/?(?:video/)?(\d+)", parsed.path)
    return match.group(1) if match else None


def render_block_html(block) -> str:
    if block is None or not block.is_active:
        return ""

    if block.content_type == block.ContentType.TEXT:
        text = apply_block_placeholders(block.text_html)
        return mark_safe(sanitize_html(text))

    if block.content_type == block.ContentType.IMAGE and block.image:
        return format_html(
            '<img class="site-block-image" src="{}" alt="{}" loading="lazy" decoding="async">',
            block.image.url,
            block.label or "",
        )

    if block.content_type == block.ContentType.VIDEO and block.video_url:
        return video_embed_html(block.video_url)

    return ""
