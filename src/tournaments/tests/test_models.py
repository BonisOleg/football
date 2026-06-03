from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from src.tournaments.models import Tournament


class TournamentModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tournaments", verbosity=0)

    def test_past_tournament_hides_countdown(self):
        tournament = Tournament.objects.get(slug="ruh-kids-cup")
        self.assertTrue(tournament.has_ended)
        self.assertFalse(tournament.show_countdown)

    def test_upcoming_tournament_shows_countdown(self):
        tournament = Tournament.objects.get(slug="leo-cup-osen")
        self.assertFalse(tournament.has_ended)
        self.assertTrue(tournament.show_countdown)

    def test_null_stats_hidden(self):
        tournament = Tournament.objects.get(slug="ruh-cup")
        self.assertFalse(tournament.show_goals_stat)
        self.assertFalse(tournament.show_wins_stat)

    def test_stats_visible_when_set(self):
        tournament = Tournament.objects.get(slug="leo-cup-osen")
        tournament.goals_count = 120
        tournament.wins_count = 48
        tournament.save(update_fields=["goals_count", "wins_count"])
        tournament.refresh_from_db()
        self.assertTrue(tournament.show_goals_stat)
        self.assertTrue(tournament.show_wins_stat)
