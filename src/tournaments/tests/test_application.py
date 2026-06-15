from datetime import datetime
from unittest.mock import patch

from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from src.tournaments.models import Application, Tournament
from src.tournaments.services import get_apply_tournaments


class ApplicationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tournaments", verbosity=0)
        cls.tournament = Tournament.objects.get(slug="fg-summer-cup")

    def test_application_post_saves_and_emails(self):
        data = {
            "tournament": self.tournament.pk,
            "team_name": "ФК Левеня",
            "age_category": "U-12",
            "coach_name": "Іван Петренко",
            "city": "Львів",
            "players_count": 12,
            "phone": "+380688902844",
            "email": "coach@example.com",
            "note": "Тестова заявка",
        }
        response = self.client.post(reverse("tournaments:apply"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("ФК Левеня", mail.outbox[0].subject)

    def test_apply_get_sets_default_tournament(self):
        fixed_now = timezone.make_aware(datetime(2026, 6, 10, 12, 0))
        with patch("django.utils.timezone.now", return_value=fixed_now):
            response = self.client.get(reverse("tournaments:apply"))
        self.assertContains(
            response,
            f'<input type="hidden" name="tournament" value="{self.tournament.pk}"',
            html=False,
        )

    def test_apply_shows_only_open_tournaments(self):
        fixed_now = timezone.make_aware(datetime(2026, 6, 10, 12, 0))
        summer = Tournament.objects.get(slug="fg-summer-cup")
        autumn = Tournament.objects.get(slug="leo-cup-osen")
        spring = Tournament.objects.get(slug="leo-cup")
        winter = Tournament.objects.get(slug="ruh-cup")
        kids = Tournament.objects.get(slug="ruh-kids-cup")

        with patch("django.utils.timezone.now", return_value=fixed_now):
            response = self.client.get(reverse("tournaments:apply"))
            open_slugs = {tournament.slug for tournament in get_apply_tournaments(at=fixed_now)}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(open_slugs, {"fg-summer-cup", "leo-cup-osen"})
        self.assertContains(response, f'data-tournament-id="{summer.pk}"')
        self.assertContains(response, f'data-tournament-id="{autumn.pk}"')
        self.assertNotContains(response, f'data-tournament-id="{spring.pk}"')
        self.assertNotContains(response, f'data-tournament-id="{winter.pk}"')
        self.assertNotContains(response, f'data-tournament-id="{kids.pk}"')

    def test_application_htmx_validation_error(self):
        response = self.client.post(
            reverse("tournaments:apply"),
            {"tournament": self.tournament.pk, "team_name": ""},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 422)
        self.assertContains(response, "Перевірте форму", status_code=422)
        self.assertContains(response, "Заповніть це поле", status_code=422)

    def test_application_htmx_success_message(self):
        data = {
            "tournament": self.tournament.pk,
            "team_name": "ФК Левеня",
            "age_category": "U-12",
            "players_count": 12,
            "phone": "+380688902844",
            "email": "coach@example.com",
        }
        response = self.client.post(
            reverse("tournaments:apply"),
            data,
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ЗАЯВКУ ПРИЙНЯТО")
        self.assertContains(response, "apply-success")
