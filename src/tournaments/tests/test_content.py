"""Tests for tournament content models and services."""

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from src.tournaments.models import (
    AgeGroup,
    ArchiveEdition,
    Goal,
    Match,
    Player,
    Team,
    Tournament,
)
from src.tournaments.services import get_bracket, get_schedule, get_top_scorers


class TournamentContentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tournaments", verbosity=0)
        cls.tournament = Tournament.objects.get(slug="leo-cup")
        cls.age = AgeGroup.objects.create(tournament=cls.tournament, name="U-12", sort_order=1)
        cls.home = Team.objects.create(
            tournament=cls.tournament,
            name="РУХ",
            city="Львів",
            short_code="РУХ",
            wins=2,
            losses=1,
        )
        cls.away = Team.objects.create(
            tournament=cls.tournament,
            name="Карпати",
            city="Львів",
            short_code="КАР",
            wins=1,
            losses=1,
        )
        cls.player = Player.objects.create(
            team=cls.home,
            age_group=cls.age,
            full_name="Тест Гравець",
        )
        cls.match = Match.objects.create(
            tournament=cls.tournament,
            home_team=cls.home,
            away_team=cls.away,
            age_group=cls.age,
            day=1,
            time=timezone.datetime(2026, 5, 15, 9, 0).time(),
            field="Поле A",
            score_home=2,
            score_away=1,
            stage=Match.Stage.GROUP,
            status=Match.Status.FINISHED,
        )
        Goal.objects.create(
            match=cls.match,
            player=cls.player,
            team=cls.home,
            minute=12,
        )

    def test_age_group_names_from_db(self):
        self.assertEqual(self.tournament.age_group_names, ["U-12"])

    def test_schedule_from_db(self):
        schedule = get_schedule(self.tournament)
        self.assertEqual(len(schedule), 1)
        self.assertEqual(schedule[0]["a"]["short"], "РУХ")

    def test_top_scorers_from_db(self):
        scorers = get_top_scorers(self.tournament)
        self.assertEqual(scorers[0]["name"], "Тест Гравець")
        self.assertEqual(scorers[0]["goals"], 1)

    def test_bracket_from_db(self):
        Match.objects.create(
            tournament=self.tournament,
            home_team=self.home,
            away_team=self.away,
            day=2,
            time=timezone.datetime(2026, 5, 16, 11, 0).time(),
            field="Поле B",
            score_home=1,
            score_away=0,
            stage=Match.Stage.R16,
            status=Match.Status.FINISHED,
        )
        bracket = get_bracket(self.tournament)
        self.assertEqual(len(bracket["r16"]), 1)


class ArchiveEditionTests(TestCase):
    def test_seed_migration_creates_archive_rows(self):
        self.assertGreaterEqual(ArchiveEdition.objects.count(), 4)
