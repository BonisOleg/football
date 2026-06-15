"""Import photos and tournament data from lvivcup.com.ua (Wix + Tournify)."""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, time as dt_time
from pathlib import Path
from typing import Any

from django.core.files.base import ContentFile
from django.db import transaction
from django.utils.text import slugify

from .models import AgeGroup, GalleryImage, Match, Player, Team, Tournament
from .services import HOME_GALLERY_TEASER_LIMIT

WIX_BASE = "https://www.lvivcup.com.ua"
WIX_MEDIA = "https://static.wixstatic.com/media"
FIRESTORE_KEY = "AIzaSyDpqIP2yOZBWjAcknp1szptkyh0fk6zGQI"
FIRESTORE_BASE = (
    "https://firestore.googleapis.com/v1/projects/tournamentsoftware-a1b3d"
    "/databases/(default)/documents"
)

WIX_PAGE_SLUGS = [
    "",
    "leo-cup",
    "ruh-cup",
    "ruh-kids-cup",
    "leo-cup-osen",
    "ruhcup",
    "ruhcup2024",
    "ruh-kids-cup-2024",
    "ruh-cup-u17-2007",
    "ruh-cup-u16-2008",
    "ruh-cup-u15-2009",
    "ruh-cup-u14-2010",
    "ruh-cup-u13-2011",
    "leo-cup-u7-2017",
    "leo-cup-u8-2016",
    "leo-cup-u9-2015",
    "leo-cup-u10-2014",
    "leo-cup-u11-2013",
    "leo-cup-u12-2012",
    "ruh-kids-cup-u-10-2014",
    "ruh-kids-cup-u-11-2013",
]

EXTRA_LIVE_LINKS = [
    "ruhcupu17",
    "ruhcupu16",
    "ruhcupu15",
    "ruhcupu14",
    "ruhcupu13",
    "leocupu2017",
    "cupleou9",
    "cupleou10",
    "cupleou11",
    "cupleou12",
    "leocupu13",
    "ruh-u10",
    "ruhu11",
]

BRANDING_ASSETS: dict[str, str] = {}

IMAGE_EXT_RE = re.compile(r"\.(jpe?g|png|webp|avif)(?:/|\?|$)", re.I)
TOURNIFY_LINK_RE = re.compile(r"tournifyapp\.com/live/([A-Za-z0-9_-]+)")
MEDIA_URL_RE = re.compile(r"static\.wixstatic\.com/media/[^\"'\s<>]+")
PLAYER_NUM_RE = re.compile(r"^№?\s*\d+\s*[-–—]?\s*")


@dataclass
class ImportStats:
    images_downloaded: int = 0
    gallery_created: int = 0
    live_links: set[str] = field(default_factory=set)
    teams_created: int = 0
    teams_updated: int = 0
    players_created: int = 0
    players_updated: int = 0
    matches_created: int = 0
    matches_updated: int = 0


def firestore_value(raw: dict[str, Any]) -> Any:
    if "stringValue" in raw:
        return raw["stringValue"]
    if "integerValue" in raw:
        return int(raw["integerValue"])
    if "doubleValue" in raw:
        return float(raw["doubleValue"])
    if "booleanValue" in raw:
        return raw["booleanValue"]
    if "nullValue" in raw:
        return None
    if "mapValue" in raw:
        fields = raw["mapValue"].get("fields", {})
        return {key: firestore_value(value) for key, value in fields.items()}
    if "arrayValue" in raw:
        return [
            firestore_value(item) for item in raw["arrayValue"].get("values", [])
        ]
    return None


def parse_document(doc: dict[str, Any]) -> dict[str, Any]:
    doc_id = doc["name"].rsplit("/", 1)[-1]
    fields = {
        key: firestore_value(value) for key, value in doc.get("fields", {}).items()
    }
    fields["_id"] = doc_id
    return fields


class TournifyClient:
    def __init__(self, pause: float = 0.15) -> None:
        self.pause = pause

    def _request(self, url: str, *, data: bytes | None = None) -> Any:
        headers = {"Content-Type": "application/json"} if data else {}
        request = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = response.read()
        if self.pause:
            time.sleep(self.pause)
        return json.loads(payload)

    def tournament_id_for_live_link(self, live_link: str) -> str | None:
        url = f"{FIRESTORE_BASE}:runQuery?key={FIRESTORE_KEY}"
        body = json.dumps(
            {
                "structuredQuery": {
                    "from": [{"collectionId": "tournaments"}],
                    "where": {
                        "fieldFilter": {
                            "field": {"fieldPath": "liveLink"},
                            "op": "EQUAL",
                            "value": {"stringValue": live_link},
                        }
                    },
                    "limit": 1,
                }
            }
        ).encode()
        rows = self._request(url, data=body)
        if not rows or "document" not in rows[0]:
            return None
        return rows[0]["document"]["name"].rsplit("/", 1)[-1]

    def list_collection(self, tournament_id: str, collection: str) -> list[dict[str, Any]]:
        docs: list[dict[str, Any]] = []
        page_token: str | None = None
        while True:
            url = (
                f"{FIRESTORE_BASE}/tournaments/{tournament_id}/{collection}"
                f"?key={FIRESTORE_KEY}&pageSize=300"
            )
            if page_token:
                url = f"{url}&pageToken={page_token}"
            payload = self._request(url)
            docs.extend(parse_document(item) for item in payload.get("documents", []))
            page_token = payload.get("nextPageToken")
            if not page_token:
                break
        return docs


def fetch_url(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()


def normalize_media_url(url: str) -> str:
    clean = url.split("?")[0]
    if clean.startswith("//"):
        clean = f"https:{clean}"
    if clean.startswith("static.wixstatic.com/"):
        clean = f"https://{clean}"
    return clean


def high_res_wix_url(url: str) -> str:
    normalized = normalize_media_url(url)
    match = re.match(
        r"(https://static\.wixstatic\.com/media/[^/]+~mv2\.(?:jpe?g|png|webp|avif))",
        normalized,
        re.I,
    )
    if match:
        base = match.group(1)
        ext = base.rsplit(".", 1)[-1].lower()
        if ext == "avif":
            return f"{base}/v1/fit/w_1600,h_1200,al_c,q_85/{base.rsplit('/', 1)[-1]}"
        return f"{base}/v1/fit/w_1600,h_1200,al_c,q_85/{base.rsplit('/', 1)[-1]}"
    return normalized


def discover_live_links() -> set[str]:
    links: set[str] = set(EXTRA_LIVE_LINKS)
    for slug in WIX_PAGE_SLUGS:
        url = f"{WIX_BASE}/{slug}" if slug else WIX_BASE
        try:
            html = fetch_url(url).decode("utf-8", errors="ignore")
        except (OSError, urllib.error.URLError):
            continue
        links.update(TOURNIFY_LINK_RE.findall(html))
        time.sleep(0.1)
    return links


def discover_wix_images() -> dict[str, str]:
    assets: dict[str, str] = {}
    for slug in WIX_PAGE_SLUGS:
        url = f"{WIX_BASE}/{slug}" if slug else WIX_BASE
        try:
            html = fetch_url(url).decode("utf-8", errors="ignore")
        except (OSError, urllib.error.URLError):
            continue
        for raw in MEDIA_URL_RE.findall(html):
            normalized = normalize_media_url(raw)
            if not IMAGE_EXT_RE.search(normalized):
                continue
            media_id = normalized.split("/media/", 1)[-1].split("/v1/", 1)[0]
            if media_id not in assets:
                assets[media_id] = high_res_wix_url(normalized)
        time.sleep(0.1)
    for filename, source in BRANDING_ASSETS.items():
        assets[filename] = source
    return assets


def tournament_slug_from_name(name: str) -> str | None:
    lowered = name.lower()
    if "kids" in lowered:
        return "ruh-kids-cup"
    if "leo" in lowered:
        return "leo-cup"
    if "ruh" in lowered:
        return "ruh-cup"
    return None


def age_group_from_name(name: str) -> str:
    match = re.search(r"U[-\s]?(\d{1,2})", name, re.I)
    if match:
        return f"U-{match.group(1)}"
    match = re.search(r"(\d{4})\s*р", name, re.I)
    if match:
        year = int(match.group(1))
        return f"U-{datetime.now().year - year}"
    digits = re.search(r"(\d{1,2})$", name.strip())
    if digits and "leo" in name.lower():
        return f"U-{digits.group(1)}"
    return name.strip()


def clean_player_name(raw_name: str) -> str:
    return PLAYER_NUM_RE.sub("", raw_name).strip()


def make_short_code(name: str) -> str:
    words = [word for word in re.split(r"\s+", name.strip()) if word]
    if len(words) >= 2:
        code = "".join(word[0] for word in words[:3]).upper()
        return code[:8] or "TM"
    cleaned = re.sub(r"[^A-Za-zА-ЯІЇЄҐ0-9]", "", name.upper())
    return (cleaned[:3] or "TM").upper()


def map_stage(round_no: int | None) -> str:
    if round_no is None:
        return Match.Stage.GROUP
    if round_no >= 4:
        return Match.Stage.FINAL
    if round_no == 3:
        return Match.Stage.SF
    if round_no == 2:
        return Match.Stage.R16
    return Match.Stage.GROUP


def build_team_lookup(teams: list[dict[str, Any]]) -> dict[str, dict[int, dict[str, Any]]]:
    lookup: dict[str, dict[int, dict[str, Any]]] = {}
    for team in teams:
        for key, poule_id in team.items():
            if not key.startswith("poule") or not isinstance(poule_id, str):
                continue
            num_key = f"numIn{key[0].upper()}{key[1:]}"
            alt_key = f"numIn{key}"
            number = team.get(num_key)
            if number is None:
                number = team.get(alt_key)
            if number is None:
                continue
            lookup.setdefault(poule_id, {})[int(number)] = team
    return lookup


class LvivcupImporter:
    def __init__(self, stdout=None, stderr=None) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self.client = TournifyClient()
        self.stats = ImportStats()

    def log(self, message: str) -> None:
        if self.stdout:
            self.stdout.write(message)

    def import_all(
        self,
        *,
        images: bool = True,
        tournaments: bool = True,
        force_images: bool = False,
    ) -> ImportStats:
        if images:
            self.import_images(force=force_images)
        if tournaments:
            self.stats.live_links = discover_live_links()
            self.log(f"Знайдено Tournify slug: {len(self.stats.live_links)}")
            for live_link in sorted(self.stats.live_links):
                self.import_live_link(live_link)
        return self.stats

    def import_images(self, *, force: bool = False) -> None:
        from django.conf import settings

        images_dir = Path(settings.BASE_DIR) / "static" / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
        media_root = Path(settings.MEDIA_ROOT) / "gallery"
        media_root.mkdir(parents=True, exist_ok=True)

        assets = discover_wix_images()
        self.log(f"Знайдено зображень на Wix: {len(assets)}")

        for index, (asset_id, url) in enumerate(sorted(assets.items()), start=1):
            ext = ".jpg"
            if ".png" in asset_id.lower():
                ext = ".png"
            elif ".webp" in asset_id.lower():
                ext = ".webp"
            elif ".avif" in asset_id.lower():
                ext = ".avif"

            if asset_id.endswith((".png", ".jpg", ".jpeg", ".webp", ".avif")):
                filename = asset_id
                dest = images_dir / filename
            else:
                filename = f"gallery/{slugify(asset_id) or f'photo-{index}'}{ext}"
                dest = images_dir / filename

            if dest.exists() and not force:
                continue
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(fetch_url(url))
                self.stats.images_downloaded += 1
            except (OSError, urllib.error.URLError) as exc:
                if self.stderr:
                    self.stderr.write(f"Не вдалося завантажити {url}: {exc}")

        existing_labels = set(
            GalleryImage.objects.values_list("label", flat=True)
        )
        sort_order = GalleryImage.objects.count()
        for path in sorted((images_dir / "gallery").glob("*")):
            if not path.is_file():
                continue
            label = path.stem.replace("-", " ").upper()
            if label in existing_labels:
                continue
            gallery = GalleryImage(
                alt_text=f"Фото турніру Football Generation — {label}",
                label=label,
                height=GalleryImage.Height.TALL if sort_order % 2 else GalleryImage.Height.SHORT,
                sort_order=sort_order,
                show_on_home=sort_order < HOME_GALLERY_TEASER_LIMIT,
                show_on_archive=True,
            )
            gallery.image.save(path.name, ContentFile(path.read_bytes()), save=True)
            existing_labels.add(label)
            sort_order += 1
            self.stats.gallery_created += 1

    @transaction.atomic
    def import_live_link(self, live_link: str) -> None:
        tournament_id = self.client.tournament_id_for_live_link(live_link)
        if not tournament_id:
            self.log(f"  · {live_link}: турнір не знайдено")
            return

        meta = self.client.list_collection(tournament_id, "teams")
        query = self.client._request(
            f"{FIRESTORE_BASE}:runQuery?key={FIRESTORE_KEY}",
            data=json.dumps(
                {
                    "structuredQuery": {
                        "from": [{"collectionId": "tournaments"}],
                        "where": {
                            "fieldFilter": {
                                "field": {"fieldPath": "liveLink"},
                                "op": "EQUAL",
                                "value": {"stringValue": live_link},
                            }
                        },
                        "limit": 1,
                    }
                }
            ).encode(),
        )
        tournify = parse_document(query[0]["document"])
        t_name = str(tournify.get("name") or live_link)
        slug = tournament_slug_from_name(t_name)
        if not slug:
            self.log(f"  · {live_link}: пропущено ({t_name})")
            return

        tournament = Tournament.objects.filter(slug=slug).first()
        if not tournament:
            self.log(f"  · {live_link}: немає Django-турніру {slug}")
            return

        age_group_name = age_group_from_name(t_name)
        age_group, _ = AgeGroup.objects.get_or_create(
            tournament=tournament,
            name=age_group_name,
            defaults={"sort_order": tournament.age_groups_rel.count()},
        )

        teams_data = self.client.list_collection(tournament_id, "teams")
        players_data = self.client.list_collection(tournament_id, "players")
        matches_data = self.client.list_collection(tournament_id, "matches")
        team_lookup = build_team_lookup(teams_data)
        django_teams: dict[str, Team] = {}

        for row in teams_data:
            name = str(row.get("name") or "").strip()
            if not name:
                continue
            short_code = make_short_code(name)
            team, created = Team.objects.update_or_create(
                tournament=tournament,
                name=name,
                defaults={
                    "city": "—",
                    "short_code": short_code,
                    "sort_order": int(row.get("numInPoule0") or 0),
                },
            )
            django_teams[row["_id"]] = team
            if created:
                self.stats.teams_created += 1
            else:
                self.stats.teams_updated += 1

        for row in players_data:
            raw_name = str(row.get("name") or "").strip()
            if not raw_name:
                continue
            team_ref = str(row.get("team") or "")
            team = django_teams.get(team_ref)
            if not team:
                continue
            full_name = clean_player_name(raw_name)
            player, created = Player.objects.update_or_create(
                team=team,
                full_name=full_name,
                defaults={
                    "age_group": age_group,
                    "sort_order": Player.objects.filter(team=team).count(),
                },
            )
            if created:
                self.stats.players_created += 1
            else:
                self.stats.players_updated += 1

        for row in matches_data:
            poule_id = row.get("poule")
            if not poule_id:
                continue
            team1_no = row.get("team1")
            team2_no = row.get("team2")
            if team1_no is None or team2_no is None:
                continue
            if int(team2_no) == 0:
                continue
            poule_map = team_lookup.get(str(poule_id), {})
            home_row = poule_map.get(int(team1_no))
            away_row = poule_map.get(int(team2_no))
            if not home_row or not away_row:
                continue
            home_team = django_teams.get(home_row["_id"])
            away_team = django_teams.get(away_row["_id"])
            if not home_team or not away_team:
                continue

            score_home = row.get("score1")
            score_away = row.get("score2")
            status = Match.Status.FINISHED
            if score_home is None or score_away is None:
                status = Match.Status.UPCOMING
                score_home = None
                score_away = None

            day = 1
            if row.get("day"):
                day = 1
            match_time = dt_time(hour=10, minute=0)
            stage = map_stage(row.get("round"))

            match, created = Match.objects.update_or_create(
                tournament=tournament,
                home_team=home_team,
                away_team=away_team,
                day=day,
                defaults={
                    "time": match_time,
                    "field": "Поле A",
                    "score_home": score_home,
                    "score_away": score_away,
                    "stage": stage,
                    "status": status,
                    "age_group": age_group,
                },
            )
            if created:
                self.stats.matches_created += 1
            else:
                self.stats.matches_updated += 1

        self._update_team_records(tournament)
        self._update_tournament_stats(tournament)
        self.log(
            f"  · {live_link} ({t_name}): "
            f"{len(teams_data)} команд, {len(players_data)} гравців, {len(matches_data)} матчів"
        )

    def _update_team_records(self, tournament: Tournament) -> None:
        for team in tournament.teams.all():
            wins = losses = 0
            for match in Match.objects.filter(
                tournament=tournament, status=Match.Status.FINISHED
            ).filter(home_team=team):
                if match.score_home is None or match.score_away is None:
                    continue
                if match.score_home > match.score_away:
                    wins += 1
                elif match.score_home < match.score_away:
                    losses += 1
            for match in Match.objects.filter(
                tournament=tournament, status=Match.Status.FINISHED
            ).filter(away_team=team):
                if match.score_home is None or match.score_away is None:
                    continue
                if match.score_away > match.score_home:
                    wins += 1
                elif match.score_away < match.score_home:
                    losses += 1
            if wins or losses:
                team.wins = wins
                team.losses = losses
                team.save(update_fields=["wins", "losses"])

    def _update_tournament_stats(self, tournament: Tournament) -> None:
        finished = Match.objects.filter(
            tournament=tournament, status=Match.Status.FINISHED
        )
        goals = wins = losses = 0
        for match in finished:
            if match.score_home is None or match.score_away is None:
                continue
            goals += int(match.score_home) + int(match.score_away)
            if match.score_home != match.score_away:
                wins += 1
                losses += 1
        tournament.teams_count = tournament.teams.count()
        tournament.matches_count = tournament.matches.count()
        tournament.goals_count = goals or None
        tournament.wins_count = wins or None
        tournament.losses_count = losses or None
        tournament.save(
            update_fields=[
                "teams_count",
                "matches_count",
                "goals_count",
                "wins_count",
                "losses_count",
            ]
        )
