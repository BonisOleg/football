from __future__ import annotations

import re

from src.tournaments.block_defaults import BLOCK_DEFAULTS
from src.tournaments.context_processors import _load_site_blocks
from src.tournaments.utils.block_placeholders import apply_block_placeholders


def _strip_html(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", text).strip()


def get_block_raw_text(page: str, key: str, *, fallback: str = "") -> str:
    block = _load_site_blocks().get(f"{page}.{key}")
    if block and block.text_html:
        return apply_block_placeholders(block.text_html.strip())
    default = BLOCK_DEFAULTS.get((page, key), fallback)
    return apply_block_placeholders(default)


def get_plain_block_text(page: str, key: str, *, fallback: str = "") -> str:
    return _strip_html(get_block_raw_text(page, key, fallback=fallback))
