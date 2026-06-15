from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from django.urls import reverse
from django.utils import timezone

from .models import Tournament

CALENDAR_AFTER_COUNT = 3
KIDS_SEASON = Tournament.SeasonIcon.KIDS


@dataclass(frozen=True)
class SeasonPresentation:
    slug: str
    title: str
    subtitle: str
    season: str
    season_en: str
    year_label: str
    theme_class: str
    dates_display: str
    starts_at: datetime
    ends_at: datetime | None
    location: str
    format_text: str
    teams_count: int
    description: str
    tagline: str
    is_virtual: bool
    hero_image_url: str | None = None

    @property
    def hero_title_parts(self) -> list[dict[str, object]]:
        if self.title.startswith("FG "):
            rest = self.title[3:].split()
            parts: list[dict[str, object]] = [
                {"text": "Football Generation", "accent": False, "brand": True},
            ]
            for word in rest:
                parts.append({"text": word, "accent": True, "brand": False})
            return parts

        words = self.title.split()
        return [
            {"text": word, "accent": index > 0, "brand": False}
            for index, word in enumerate(words)
        ]

    def show_countdown_at(self, at: datetime) -> bool:
        return at < (self.ends_at or self.starts_at)


@dataclass
class SeasonSlot:
    presentation: SeasonPresentation
    is_past: bool
    is_virtual: bool
    wheel_index: int = 0
    db_tournament: Tournament | None = None

    @property
    def detail_url(self) -> str | None:
        if self.is_virtual or self.db_tournament is None:
            return None
        return self.db_tournament.get_absolute_url()

    @property
    def apply_url(self) -> str:
        return f"{reverse('tournaments:apply')}?tournament={self.presentation.slug}"


def year_label_for(season_en: str, starts_at: datetime) -> str:
    year = starts_at.year
    if season_en == Tournament.SeasonIcon.WINTER:
        return f"{year - 1}-{year}"
    return str(year)


def shift_datetime_year(dt: datetime, delta: int) -> datetime:
    target_year = dt.year + delta
    try:
        return dt.replace(year=target_year)
    except ValueError:
        return dt.replace(year=target_year, day=28)


def edition_datetimes(
    template: Tournament,
    edition_start_year: int,
) -> tuple[datetime, datetime | None]:
    delta = edition_start_year - template.starts_at.year
    starts = shift_datetime_year(template.starts_at, delta)
    ends = shift_datetime_year(template.ends_at, delta) if template.ends_at else None
    return starts, ends


def shift_dates_display(text: str, template_year: int, target_year: int) -> str:
    return text.replace(str(template_year), str(target_year))


def _slot_identity(slot: SeasonSlot) -> tuple[str, int]:
    return (slot.presentation.season_en, slot.presentation.starts_at.year)


def _forward_ahead_counts(slots: list[SeasonSlot], active_idx: int) -> tuple[int, bool]:
    non_kids = 0
    has_kids = False
    for slot in slots[active_idx + 1 :]:
        if slot.presentation.season_en == KIDS_SEASON:
            has_kids = True
        else:
            non_kids += 1
    return non_kids, has_kids


def _forward_window_satisfied(slots: list[SeasonSlot], active_idx: int) -> bool:
    non_kids, has_kids = _forward_ahead_counts(slots, active_idx)
    return non_kids >= CALENDAR_AFTER_COUNT and has_kids


def get_calendar_season_slots(
    slots: list[SeasonSlot],
    at: datetime | None = None,
) -> list[SeasonSlot]:
    at = at or timezone.now()
    if not slots:
        return []

    active_idx = active_wheel_index(slots, at=at)
    current = slots[active_idx]
    result = [current]
    seen = {_slot_identity(current)}

    non_kids_added = 0
    for slot in slots[active_idx + 1 :]:
        if non_kids_added >= CALENDAR_AFTER_COUNT:
            break
        if slot.presentation.season_en == KIDS_SEASON:
            continue
        ident = _slot_identity(slot)
        if ident not in seen:
            result.append(slot)
            seen.add(ident)
            non_kids_added += 1

    for slot in slots[active_idx + 1 :]:
        if slot.presentation.season_en == KIDS_SEASON and not slot.is_past:
            ident = _slot_identity(slot)
            if ident not in seen:
                result.append(slot)
            break

    result.sort(key=lambda item: item.presentation.starts_at)
    return result


def _trim_wheel_slots(slots: list[SeasonSlot], at: datetime) -> list[SeasonSlot]:
    calendar = get_calendar_season_slots(slots, at=at)
    calendar_ids = {_slot_identity(slot) for slot in calendar}
    trimmed = [
        slot for slot in slots if slot.is_past or _slot_identity(slot) in calendar_ids
    ]
    for index, slot in enumerate(trimmed):
        slot.wheel_index = index
    return trimmed


def _slot_key(season_en: str, starts_at: datetime) -> tuple[str, int]:
    return (season_en, starts_at.year)


def _ends_at_or_starts_at(starts_at: datetime, ends_at: datetime | None) -> datetime:
    return ends_at or starts_at


def _hero_image_url(tournament: Tournament) -> str | None:
    if tournament.hero_image:
        return tournament.hero_image.url
    return None


def _presentation_from_db(tournament: Tournament) -> SeasonPresentation:
    return SeasonPresentation(
        slug=tournament.slug,
        title=tournament.title,
        subtitle=tournament.subtitle,
        season=tournament.season,
        season_en=tournament.season_en,
        year_label=year_label_for(tournament.season_en, tournament.starts_at),
        theme_class=tournament.theme_class,
        dates_display=tournament.dates_display,
        starts_at=tournament.starts_at,
        ends_at=tournament.ends_at,
        location=tournament.location,
        format_text=tournament.format_text,
        teams_count=tournament.teams_count,
        description=tournament.description,
        tagline=tournament.tagline,
        is_virtual=False,
        hero_image_url=_hero_image_url(tournament),
    )


def _presentation_from_template(
    template: Tournament,
    starts_at: datetime,
    ends_at: datetime | None,
) -> SeasonPresentation:
    template_year = template.starts_at.year
    target_year = starts_at.year
    return SeasonPresentation(
        slug=template.slug,
        title=template.title,
        subtitle=template.subtitle,
        season=template.season,
        season_en=template.season_en,
        year_label=year_label_for(template.season_en, starts_at),
        theme_class=template.theme_class,
        dates_display=shift_dates_display(template.dates_display, template_year, target_year),
        starts_at=starts_at,
        ends_at=ends_at,
        location=template.location,
        format_text=template.format_text,
        teams_count=template.teams_count,
        description=template.description,
        tagline=template.tagline,
        is_virtual=True,
        hero_image_url=_hero_image_url(template),
    )


def _next_edition_after(
    cycle: list[Tournament],
    after: datetime,
) -> tuple[Tournament, datetime, datetime | None] | None:
    candidates: list[tuple[datetime, Tournament, datetime | None]] = []

    for template in cycle:
        for year in range(after.year, after.year + 3):
            starts, ends = edition_datetimes(template, year)
            if starts > after:
                candidates.append((starts, template, ends))

    if not candidates:
        return None

    starts, template, ends = min(candidates, key=lambda item: item[0])
    return template, starts, ends


def _load_cycle_templates() -> list[Tournament]:
    templates = list(Tournament.objects.filter(is_published=True))
    return sorted(templates, key=lambda item: (item.starts_at.month, item.starts_at.day, item.sort_order))


def presentation_from_db(tournament: Tournament) -> SeasonPresentation:
    return _presentation_from_db(tournament)


def build_season_timeline(
    at: datetime | None = None,
) -> list[SeasonSlot]:
    at = at or timezone.now()
    cycle = _load_cycle_templates()
    if not cycle:
        return []

    slots_by_key: dict[tuple[str, int], SeasonSlot] = {}

    for tournament in Tournament.objects.filter(is_published=True).order_by("starts_at"):
        ends = _ends_at_or_starts_at(tournament.starts_at, tournament.ends_at)
        key = _slot_key(tournament.season_en, tournament.starts_at)
        slots_by_key[key] = SeasonSlot(
            presentation=_presentation_from_db(tournament),
            is_past=at >= ends,
            is_virtual=False,
            db_tournament=tournament,
        )

    ordered = sorted(
        slots_by_key.values(),
        key=lambda slot: slot.presentation.starts_at,
    )

    active_idx = active_wheel_index(ordered, at=at)

    if ordered:
        cursor_end = _ends_at_or_starts_at(
            ordered[-1].presentation.starts_at,
            ordered[-1].presentation.ends_at,
        )
    else:
        cursor_end = at

    while not _forward_window_satisfied(ordered, active_idx):
        nxt = _next_edition_after(cycle, cursor_end)
        if nxt is None:
            break

        template, starts, ends = nxt
        key = _slot_key(template.season_en, starts)
        if key in slots_by_key:
            cursor_end = _ends_at_or_starts_at(starts, ends)
            continue

        slot = SeasonSlot(
            presentation=_presentation_from_template(template, starts, ends),
            is_past=at >= _ends_at_or_starts_at(starts, ends),
            is_virtual=True,
            db_tournament=None,
        )
        slots_by_key[key] = slot
        ordered.append(slot)
        ordered.sort(key=lambda item: item.presentation.starts_at)
        cursor_end = _ends_at_or_starts_at(starts, ends)

    return _trim_wheel_slots(ordered, at)


def active_wheel_index(slots: list[SeasonSlot], at: datetime | None = None) -> int:
    at = at or timezone.now()
    for index, slot in enumerate(slots):
        ends = _ends_at_or_starts_at(slot.presentation.starts_at, slot.presentation.ends_at)
        if at < ends:
            return index
    return max(len(slots) - 1, 0)


def get_home_season_timeline(
    at: datetime | None = None,
) -> tuple[list[SeasonSlot], int]:
    at = at or timezone.now()
    slots = build_season_timeline(at=at)
    return slots, active_wheel_index(slots, at=at)


def get_upcoming_season_slots(
    slots: list[SeasonSlot],
    at: datetime | None = None,
) -> list[SeasonSlot]:
    return get_calendar_season_slots(slots, at=at)


def find_wheel_slot(
    slug: str,
    *,
    edition_year: int | None = None,
    at: datetime | None = None,
) -> SeasonSlot | None:
    slots, _ = get_home_season_timeline(at=at)
    for slot in slots:
        if slot.presentation.slug != slug:
            continue
        if edition_year is None:
            return slot
        if slot.presentation.starts_at.year == edition_year:
            return slot
    return None
