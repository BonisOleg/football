from __future__ import annotations

from collections import defaultdict
from typing import Any

from .models import GalleryImage, Goal, Match, Team, Tournament

HOME_GALLERY_TEASER_LIMIT = 6


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
