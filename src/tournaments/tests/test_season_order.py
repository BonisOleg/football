from datetime import datetime, timezone as dt_timezone
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from src.tournaments.models import Tournament
from src.tournaments.services import (
    calendar_season_for_month,
    get_apply_tournaments,
    get_published_tournaments,
    order_tournaments_by_current_season,
)


class SeasonOrderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tournaments", verbosity=0)

    def test_calendar_season_for_month(self):
        self.assertEqual(calendar_season_for_month(3), Tournament.SeasonIcon.SPRING)
        self.assertEqual(calendar_season_for_month(6), Tournament.SeasonIcon.SUMMER)
        self.assertEqual(calendar_season_for_month(10), Tournament.SeasonIcon.AUTUMN)
        self.assertEqual(calendar_season_for_month(1), Tournament.SeasonIcon.WINTER)

    def test_summer_starts_first_in_june(self):
        at = datetime(2026, 6, 10, 12, 0, tzinfo=dt_timezone.utc)
        ordered = get_published_tournaments(at=at)
        self.assertEqual(ordered[0].slug, "fg-summer-cup")
        self.assertEqual([t.season_en for t in ordered[:4]], ["Summer", "Autumn", "Winter", "Spring"])
        self.assertEqual(ordered[-1].slug, "ruh-kids-cup")

    def test_apply_tournaments_exclude_past_events(self):
        at = datetime(2026, 6, 10, 12, 0, tzinfo=dt_timezone.utc)
        ordered = get_apply_tournaments(at=at)
        self.assertEqual([t.slug for t in ordered], ["fg-summer-cup", "leo-cup-osen"])

    def test_spring_starts_first_in_april(self):
        at = datetime(2026, 4, 1, 12, 0, tzinfo=dt_timezone.utc)
        ordered = get_published_tournaments(at=at)
        self.assertEqual(ordered[0].slug, "leo-cup")

    def test_winter_starts_first_in_january(self):
        at = datetime(2026, 1, 15, 12, 0, tzinfo=dt_timezone.utc)
        ordered = get_published_tournaments(at=at)
        self.assertEqual(ordered[0].slug, "ruh-cup")

    def test_home_active_tournament_matches_current_season(self):
        fixed_now = timezone.make_aware(datetime(2026, 6, 10, 12, 0))
        with patch("django.utils.timezone.now", return_value=fixed_now):
            response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FG SUMMER CUP")
        self.assertContains(response, 'data-initial-wheel-index="3"')

    def test_order_tournaments_keeps_kids_last(self):
        tournaments = list(Tournament.objects.filter(is_published=True))
        at = datetime(2026, 9, 1, 12, 0, tzinfo=dt_timezone.utc)
        ordered = order_tournaments_by_current_season(tournaments, at=at)
        self.assertEqual(ordered[0].season_en, Tournament.SeasonIcon.AUTUMN)
        self.assertEqual(ordered[-1].season_en, Tournament.SeasonIcon.KIDS)
