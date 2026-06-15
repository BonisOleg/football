from datetime import datetime
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from src.tournaments.models import Tournament
from src.tournaments.season_timeline import (
    active_wheel_index,
    get_calendar_season_slots,
    get_home_season_timeline,
    year_label_for,
)


class SeasonTimelineTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tournaments", verbosity=0)

    def _at(self, year: int, month: int, day: int) -> datetime:
        return timezone.make_aware(datetime(year, month, day, 12, 0))

    def test_year_label_winter_span(self):
        starts = self._at(2027, 1, 23)
        self.assertEqual(year_label_for(Tournament.SeasonIcon.WINTER, starts), "2026-2027")

    def test_year_label_spring_single(self):
        starts = self._at(2027, 5, 15)
        self.assertEqual(year_label_for(Tournament.SeasonIcon.SPRING, starts), "2027")

    def test_june_2026_active_is_summer(self):
        at = self._at(2026, 6, 10)
        slots, active = get_home_season_timeline(at=at)
        self.assertEqual(slots[active].presentation.slug, "fg-summer-cup")
        self.assertEqual(slots[active].presentation.year_label, "2026")

    def test_june_2026_wheel_includes_past_seasons(self):
        at = self._at(2026, 6, 10)
        slots, active = get_home_season_timeline(at=at)
        slugs_before_active = [slot.presentation.slug for slot in slots[:active]]
        self.assertIn("leo-cup", slugs_before_active)
        self.assertIn("ruh-cup", slugs_before_active)
        self.assertTrue(all(slot.is_past for slot in slots[:active]))

    def test_june_2026_calendar_shows_current_plus_three_and_kids(self):
        at = self._at(2026, 6, 10)
        slots, active = get_home_season_timeline(at=at)
        calendar = get_calendar_season_slots(slots, at=at)

        self.assertEqual(calendar[0].presentation.slug, "fg-summer-cup")
        self.assertEqual(calendar[0].presentation.starts_at.year, 2026)
        self.assertEqual(len(calendar), 5)

        summer_years = [
            slot.presentation.starts_at.year
            for slot in calendar
            if slot.presentation.slug == "fg-summer-cup"
        ]
        self.assertEqual(summer_years, [2026])

        kids_slots = [
            slot for slot in calendar if slot.presentation.season_en == Tournament.SeasonIcon.KIDS
        ]
        self.assertEqual(len(kids_slots), 1)
        self.assertGreater(kids_slots[0].presentation.starts_at.year, 2026)

    def test_june_2026_calendar_excludes_past(self):
        at = self._at(2026, 6, 10)
        slots, _ = get_home_season_timeline(at=at)
        calendar = get_calendar_season_slots(slots, at=at)
        past_spring_2026 = [
            slot
            for slot in calendar
            if slot.presentation.slug == "leo-cup"
            and slot.presentation.starts_at.year == 2026
        ]
        self.assertEqual(past_spring_2026, [])
        slugs = [slot.presentation.slug for slot in calendar]
        self.assertIn("fg-summer-cup", slugs)

    def test_june_2026_wheel_does_not_project_beyond_window(self):
        at = self._at(2026, 6, 10)
        slots, _ = get_home_season_timeline(at=at)
        summer_2027 = [
            slot
            for slot in slots
            if slot.presentation.slug == "fg-summer-cup"
            and slot.presentation.starts_at.year == 2027
        ]
        self.assertEqual(summer_2027, [])

    def test_june_2026_projects_virtual_winter_after_autumn(self):
        at = self._at(2026, 6, 10)
        slots, _ = get_home_season_timeline(at=at)
        autumn_idx = next(
            i for i, slot in enumerate(slots) if slot.presentation.slug == "leo-cup-osen"
        )
        winter_next = slots[autumn_idx + 1]
        self.assertEqual(winter_next.presentation.slug, "ruh-cup")
        self.assertTrue(winter_next.is_virtual)
        self.assertEqual(winter_next.presentation.year_label, "2026-2027")

    def test_may_2027_active_is_spring(self):
        at = self._at(2027, 5, 15)
        slots, active = get_home_season_timeline(at=at)
        self.assertEqual(slots[active].presentation.slug, "leo-cup")
        self.assertEqual(slots[active].presentation.starts_at.year, 2027)

    def test_db_record_overrides_virtual(self):
        Tournament.objects.create(
            slug="leo-cup-2027",
            title="FG SPRING CUP",
            subtitle="Spring Edition",
            season="Весна",
            season_en=Tournament.SeasonIcon.SPRING,
            year="2027",
            theme_class=Tournament.ThemeClass.SPRING,
            dates_display="14 — 16 травня 2027",
            starts_at=self._at(2027, 5, 14),
            ends_at=self._at(2027, 5, 16),
            location="СК «Сокіл», Львів",
            teams_count=64,
            matches_count=96,
            format_text="8+1, два тайми по 20 хв",
            prize="Кубки",
            fee_uah="4 200",
            description="Весна 2027",
            highlight="Test",
            tagline="Test",
            is_published=True,
            sort_order=1,
        )
        at = self._at(2026, 6, 10)
        slots, _ = get_home_season_timeline(at=at)
        spring_2027 = next(
            slot
            for slot in slots
            if slot.presentation.season_en == Tournament.SeasonIcon.SPRING
            and slot.presentation.starts_at.year == 2027
        )
        self.assertFalse(spring_2027.is_virtual)
        self.assertEqual(spring_2027.presentation.slug, "leo-cup-2027")

    def test_home_renders_timeline_active_summer(self):
        fixed_now = self._at(2026, 6, 10)
        with patch("django.utils.timezone.now", return_value=fixed_now):
            response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-initial-wheel-index="3"')
        self.assertContains(response, "FG SUMMER CUP")
        self.assertContains(response, "2026-2027")

    def test_active_wheel_index_first_not_ended(self):
        at = self._at(2026, 6, 10)
        slots, active = get_home_season_timeline(at=at)
        self.assertEqual(active, active_wheel_index(slots, at=at))
        self.assertFalse(slots[active].is_past)
