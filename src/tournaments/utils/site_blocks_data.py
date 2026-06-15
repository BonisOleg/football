from __future__ import annotations

import re

from src.tournaments.mock_data import MARQUEE_ITEMS
from src.tournaments.models import SiteBlock
from src.tournaments.utils.html import sanitize_html

DEFAULT_HUB_STATS: tuple[dict[str, str | int], ...] = (
    {"value": 208, "label": "Команд за рік", "hint": "ACROSS 5 EVENTS"},
    {"value": 316, "label": "Матчів", "hint": "REGULAR + PLAYOFF"},
    {"value": 1381, "label": "Голів", "hint": "2025 SEASON"},
    {"value": 28, "label": "Міст-учасників", "hint": "UA + EU"},
)


def _block_text(blocks: dict[str, SiteBlock], page: str, key: str) -> str:
    block = blocks.get(f"{page}.{key}")
    if block and block.text_html.strip():
        return block.text_html.strip()
    return ""


def _block_inline_html(blocks: dict[str, SiteBlock], page: str, key: str, fallback: str = "") -> str:
    raw = _block_text(blocks, page, key) or fallback
    if not raw:
        return ""
    return sanitize_html(raw)


def get_marquee_items(blocks: dict[str, SiteBlock]) -> list[str]:
    raw = _block_text(blocks, "home", "marquee")
    if raw:
        items = [line.strip() for line in raw.splitlines() if line.strip()]
        if items:
            return items
    return list(MARQUEE_ITEMS)


def _parse_stat_value(raw: str, fallback: int) -> int:
    plain = re.sub(r"<[^>]+>", " ", raw or "")
    cleaned = plain.strip().replace(" ", "").replace("+", "")
    if not cleaned:
        return fallback
    try:
        return int(cleaned)
    except ValueError:
        return fallback


def get_hub_stats(blocks: dict[str, SiteBlock]) -> list[dict[str, str | int]]:
    stats: list[dict[str, str | int]] = []
    for index, default in enumerate(DEFAULT_HUB_STATS, start=1):
        prefix = f"stat_{index}"
        value_raw = _block_text(blocks, "home", f"{prefix}_value")
        label = _block_inline_html(blocks, "home", f"{prefix}_label", str(default["label"]))
        hint = _block_inline_html(blocks, "home", f"{prefix}_hint", str(default["hint"]))
        value = _parse_stat_value(value_raw, int(default["value"]))
        stats.append({"value": value, "label": label, "hint": hint})
    return stats
