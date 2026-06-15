from django.core.management import call_command
from django.test import TestCase

from src.tournaments.models import Tournament


class FixtureTests(TestCase):
    def test_five_tournaments_loaded(self):
        call_command("loaddata", "tournaments", verbosity=0)
        self.assertEqual(Tournament.objects.filter(is_published=True).count(), 5)
