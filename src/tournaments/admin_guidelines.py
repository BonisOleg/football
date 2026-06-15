from dataclasses import dataclass

from django.utils.html import format_html, format_html_join
from django.utils.safestring import SafeString, mark_safe

ACCENT_SPAN_BLOCK_KEYS = frozenset({
    "stats_title",
    "hero_title",
    "editions_title",
    "gallery_title",
    "cta_title",
})

TEXT_MAX_LENGTHS = {
    "text_html": 5000,
    "description": 8000,
    "footer_about": 500,
    "header_cta_label": 64,
    "site_label": 64,
    "stat_value": 16,
    "block_paragraph": 500,
    "tagline": 128,
    "highlight": 256,
}


@dataclass(frozen=True)
class ImageProfile:
    max_bytes: int
    min_width: int | None = None
    max_width: int | None = None
    max_height: int | None = None
    recommended: str = ""
    formats: str = "JPG, WebP або PNG"


IMAGE_PROFILES: dict[str, ImageProfile] = {
    "siteblock_image": ImageProfile(
        max_bytes=2 * 1024 * 1024,
        min_width=600,
        recommended="1600×900 px",
    ),
    "tournament_hero": ImageProfile(
        max_bytes=3 * 1024 * 1024,
        min_width=1200,
        recommended="1920×1080 px (16:9)",
    ),
    "tournament_card": ImageProfile(
        max_bytes=int(1.5 * 1024 * 1024),
        min_width=400,
        recommended="800×600 px",
    ),
    "gallery": ImageProfile(
        max_bytes=2 * 1024 * 1024,
        min_width=600,
        recommended="1200×800 px (альбомна орієнтація)",
    ),
    "logo": ImageProfile(
        max_bytes=500 * 1024,
        max_width=800,
        max_height=800,
        recommended="до 400×400 px, PNG з прозорим фоном",
        formats="PNG, WebP або SVG",
    ),
}

CALLOUT_CONTENT: dict[str, dict[str, list[str]]] = {
    "siteblock": {
        "title": "Увага: зміни в цьому блоці можуть зламати вигляд сторінки",
        "items": [
            "Короткі рядки (мітки, числа, кнопки, підписи) — один рядок звичайного тексту без HTML.",
            "Описи та бігучий рядок — кілька рядків без HTML. У бігучому рядку кожен пункт з нового рядка.",
            "Для заголовків stats_title, hero_title, editions_title і gallery_title можна виділити акцент: "
            '<code>&lt;span class="text-accent"&gt;…&lt;/span&gt;</code>. Інший HTML заборонений.',
            "У текстах банера можна підставити {year}, {season_start}, {season_end}.",
            "Фото: до 2 MB, ширина від 600 px, рекомендовано 1600×900 px.",
            "Відео: лише посилання YouTube або Vimeo. Файли .mp4 завантажувати не можна.",
            "Неправильний контент блокує збереження форми.",
        ],
    },
    "sitesettings": {
        "title": "Увага: ці налаштування впливають на весь сайт",
        "items": [
            "Логотип: до 500 KB, максимум 800×800 px. Великий файл сповільнює завантаження.",
            "Текст про організацію — лише звичайний текст без HTML.",
            "Copyright: короткий рядок, використовуйте {year} для поточного року.",
            "Довгі тексти можуть зламати футер або хедер на мобільних.",
        ],
    },
    "tournament": {
        "title": "Увага: контент турніру формує головний екран сторінки",
        "items": [
            "Опис: лише безпечне форматування (жирний, курсив, списки, посилання).",
            "Hero-фото: до 3 MB, ширина від 1200 px, рекомендовано 1920×1080 px.",
            "Фото картки: до 1.5 MB, ширина від 400 px, рекомендовано 800×600 px.",
            "Короткі поля (слоган, акцент) не розтягуйте — довгий текст ламає сітку.",
        ],
    },
    "gallery": {
        "title": "Увага: фото галереї впливають на сітку головної та архіву",
        "items": [
            "Фото: до 2 MB, ширина від 600 px, рекомендовано альбомне 1200×800 px.",
            "Висота блоку (240 або 320 px) змінює розмір плитки в галереї.",
            "Завантажуйте однаково якісні фото — різний формат ламає сітку.",
        ],
    },
}

FIELD_HELP: dict[str, str] = {
    "text_html": (
        "Лише звичайний текст або, для заголовків з акцентом, "
        '<span class="text-accent">…</span>. Без картинок, відео та зайвого HTML. Максимум 5000 символів.'
    ),
    "siteblock_image": (
        "До 2 MB · ширина від 600 px · рекомендовано 1600×900 px · JPG/WebP/PNG"
    ),
    "video_url": (
        "Лише YouTube або Vimeo. Приклад: https://www.youtube.com/watch?v=… "
        "або https://vimeo.com/123456789"
    ),
    "logo": "До 500 KB · максимум 800×800 px · рекомендовано PNG до 400×400 px",
    "footer_about": "Лише звичайний текст без HTML. Максимум 500 символів.",
    "footer_copyright": "Короткий рядок. Використовуйте {year} для року.",
    "header_cta_label": "Короткий текст кнопки. Максимум 64 символи.",
    "site_label": "Короткий підпис без HTML. Максимум 64 символи.",
    "stat_value": "Лише цифра без HTML. Наприклад: 208",
    "block_paragraph": "Звичайний текст без HTML. Для бігучого рядка — один пункт з нового рядка.",
    "description": (
        "Дозволено: жирний/курсив, списки, посилання. Без картинок і відео. Максимум 8000 символів."
    ),
    "hero_image": "До 3 MB · ширина від 1200 px · рекомендовано 1920×1080 px (16:9)",
    "card_image": "До 1.5 MB · ширина від 400 px · рекомендовано 800×600 px",
    "gallery_image": "До 2 MB · ширина від 600 px · рекомендовано 1200×800 px",
    "gallery_height": "240 px — нижча плитка, 320 px — вища. Впливає на сітку галереї.",
    "tagline": "Короткий слоган. Максимум 128 символів — довший текст ламає картку.",
    "highlight": "Короткий акцент. Максимум 256 символів.",
}


def format_file_size(num_bytes: int) -> str:
    if num_bytes >= 1024 * 1024:
        value = num_bytes / (1024 * 1024)
        return f"{value:.1f} MB" if value % 1 else f"{int(value)} MB"
    value = num_bytes / 1024
    return f"{int(value)} KB"


def field_help(key: str) -> str:
    return FIELD_HELP.get(key, "")


def render_admin_warning_callout(profile: str) -> SafeString:
    content = CALLOUT_CONTENT[profile]
    items_html = format_html_join(
        "",
        "<li>{}</li>",
        ((mark_safe(item),) for item in content["items"]),
    )
    return format_html(
        '<div class="admin-content-warning" role="alert">'
        '<div class="admin-content-warning__title">⚠ {}</div>'
        '<ul class="admin-content-warning__list">{}</ul>'
        "</div>",
        content["title"],
        items_html,
    )
