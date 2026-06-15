from __future__ import annotations

from django.utils import timezone

UKR_MONTHS = (
    "січня",
    "лютого",
    "березня",
    "квітня",
    "травня",
    "червня",
    "липня",
    "серпня",
    "вересня",
    "жовтня",
    "листопада",
    "грудня",
)


def format_uk_date(value) -> str:
    if not value:
        return "—"
    return f"{value.day} {UKR_MONTHS[value.month - 1]} {value.year}"


def apply_block_placeholders(text: str, site_settings=None) -> str:
    if not text:
        return text

    if site_settings is None:
        from src.tournaments.models import SiteSettings

        site_settings = SiteSettings.load()

    replacements = {
        "year": str(timezone.now().year),
        "season_start": format_uk_date(site_settings.season_start),
        "season_end": format_uk_date(site_settings.season_end),
    }

    result = text
    for key, value in replacements.items():
        result = result.replace(f"{{{key}}}", value)
    return result
