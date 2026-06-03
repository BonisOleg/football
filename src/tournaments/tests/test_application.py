from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from src.tournaments.models import Application, Tournament


class ApplicationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tournaments", verbosity=0)
        cls.tournament = Tournament.objects.get(slug="leo-cup")

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
        response = self.client.get(reverse("tournaments:apply"))
        self.assertContains(
            response,
            f'<input type="hidden" name="tournament" value="{self.tournament.pk}"',
            html=False,
        )

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
