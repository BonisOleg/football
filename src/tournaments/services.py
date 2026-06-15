from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any

from django.db.models import QuerySet
from django.utils import timezone

from .models import GalleryImage, Goal, Match, Team, Tournament

HOME_GALLERY_TEASER_LIMIT = 6

CALENDAR_SEASONS: tuple[str, ...] = (
    Tournament.SeasonIcon.SPRING,
    Tournament.SeasonIcon.SUMMER,
    Tournament.SeasonIcon.AUTUMN,
    Tournament.SeasonIcon.WINTER,
)


def calendar_season_for_month(month: int) -> str:
    if month in (3, 4, 5):
        return Tournament.SeasonIcon.SPRING
    if month in (6, 7, 8):
        return Tournament.SeasonIcon.SUMMER
    if month in (9, 10, 11):
        return Tournament.SeasonIcon.AUTUMN
    return Tournament.SeasonIcon.WINTER


def order_tournaments_by_current_season(
    tournaments: list[Tournament] | QuerySet[Tournament],
    *,
    at: datetime | None = None,
) -> list[Tournament]:
    items = list(tournaments)
    if not items:
        return []

    at = at or timezone.now()
    current_season = calendar_season_for_month(at.month)

    main = [t for t in items if t.season_en in CALENDAR_SEASONS]
    extras = [t for t in items if t.season_en not in CALENDAR_SEASONS]

    base_rank = {season: index for index, season in enumerate(CALENDAR_SEASONS)}
    main.sort(key=lambda t: (base_rank.get(t.season_en, 99), t.sort_order, t.starts_at))

    start_idx = CALENDAR_SEASONS.index(current_season)
    rotated = CALENDAR_SEASONS[start_idx:] + CALENDAR_SEASONS[:start_idx]
    display_rank = {season: index for index, season in enumerate(rotated)}

    main.sort(key=lambda t: (display_rank.get(t.season_en, 99), t.sort_order, t.starts_at))
    extras.sort(key=lambda t: (t.sort_order, t.starts_at))

    return main + extras


def get_published_tournaments(*, at: datetime | None = None) -> list[Tournament]:
    queryset = Tournament.objects.filter(is_published=True)
    return order_tournaments_by_current_season(queryset, at=at)


def tournament_apply_deadline(tournament: Tournament) -> datetime:
    return tournament.ends_at or tournament.starts_at


def tournament_is_open_for_apply(tournament: Tournament, *, at: datetime | None = None) -> bool:
    at = at or timezone.now()
    return at < tournament_apply_deadline(tournament)


def filter_open_tournaments(
    tournaments: list[Tournament] | QuerySet[Tournament],
    *,
    at: datetime | None = None,
) -> list[Tournament]:
    at = at or timezone.now()
    return [tournament for tournament in tournaments if tournament_is_open_for_apply(tournament, at=at)]


def get_apply_tournaments(*, at: datetime | None = None) -> list[Tournament]:
    return filter_open_tournaments(get_published_tournaments(at=at), at=at)


def team_dict(team: Team) -> dict[str, str]:
    return {"name": team.name, "city": team.city, "short": team.short_code}


def match_pair_dict(match: Match) -> dict[str, Any]:
    return {
        "a": team_dict(match.home_team),
        "b": team_dict(match.away_team),
        "sA": match.score_home if match.score_home is not None else "–",
        "sB": match.score_away if match.score_away is not None else "–",
        "status": match.status,
    }


def get_teams_pool(tournament: Tournament) -> list[dict[str, str]]:
    teams = tournament.teams.order_by("sort_order", "name")
    if teams.exists():
        return [team_dict(team) for team in teams]
    return []


def get_schedule(tournament: Tournament) -> list[dict[str, Any]]:
    matches = (
        tournament.matches.select_related("home_team", "away_team", "age_group")
        .exclude(stage=Match.Stage.FINAL)
        .order_by("day", "time", "pk")
    )
    if not matches.exists():
        return []

    rows: list[dict[str, Any]] = []
    for match in matches:
        if match.stage in {Match.Stage.R16, Match.Stage.SF}:
            continue
        age = match.age_group.name if match.age_group else "—"
        rows.append(
            {
                "day": match.day,
                "time": match.time_display,
                "field": match.field,
                "a": team_dict(match.home_team),
                "b": team_dict(match.away_team),
                "age": age,
                "status": match.status,
                "sA": match.score_home,
                "sB": match.score_away,
            }
        )
    return rows


def get_bracket(tournament: Tournament) -> dict[str, Any]:
    empty_final = {
        "a": {"name": "—", "city": "", "short": "—"},
        "b": {"name": "—", "city": "", "short": "—"},
        "sA": "–",
        "sB": "–",
        "status": "upcoming",
    }
    bracket = {"r16": [], "sf": [], "final": empty_final}

    stage_map = {
        Match.Stage.R16: "r16",
        Match.Stage.SF: "sf",
        Match.Stage.FINAL: "final",
    }
    matches = tournament.matches.select_related("home_team", "away_team").filter(
        stage__in=stage_map
    )
    if not matches.exists():
        return bracket

    for match in matches.order_by("pk"):
        key = stage_map[match.stage]
        payload = match_pair_dict(match)
        if key == "final":
            bracket["final"] = payload
        else:
            bracket[key].append(payload)
    return bracket


def get_top_scorers(tournament: Tournament) -> list[dict[str, Any]]:
    goals = (
        Goal.objects.filter(match__tournament=tournament, player__isnull=False)
        .select_related("player", "player__team", "player__age_group")
        .order_by("player_id")
    )
    if not goals.exists():
        return []

    counts: dict[int, int] = defaultdict(int)
    players: dict[int, Any] = {}
    for goal in goals:
        counts[goal.player_id] += 1
        players[goal.player_id] = goal.player

    ranked = sorted(counts.items(), key=lambda item: (-item[1], players[item[0]].full_name))
    rows: list[dict[str, Any]] = []
    for player_id, total in ranked:
        player = players[player_id]
        age = player.age_group.name if player.age_group else "—"
        rows.append(
            {
                "name": player.full_name,
                "team": player.team.short_code,
                "age": age,
                "goals": total,
            }
        )
    return rows


def get_gallery_teaser() -> list[GalleryImage]:
    return list(
        GalleryImage.objects.filter(show_on_home=True).order_by("sort_order", "pk")[
            :HOME_GALLERY_TEASER_LIMIT
        ]
    )


def get_archive_gallery() -> list[GalleryImage]:
    return list(GalleryImage.objects.filter(show_on_archive=True).order_by("sort_order", "pk"))
