from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tournaments", verbosity=0)

    def test_home_ok(self):
        response = self.client.get(reverse("tournaments:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "RUH LEO CUP")

    def test_home_hides_countdown_for_past_tournament(self):
        response = self.client.get(reverse("tournaments:home"))
        self.assertNotContains(response, 'data-starts-at="2026-02-06')
        self.assertContains(response, 'data-starts-at="2026-10-10')

    def test_detail_hides_goals_when_empty(self):
        response = self.client.get(reverse("tournaments:detail", kwargs={"slug": "ruh-kids-cup"}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Голів")
        self.assertNotContains(response, "Перемог")

    def test_tournament_slugs_ok(self):
        for slug in ("leo-cup", "leo-cup-osen", "ruh-cup", "ruh-kids-cup"):
            url = reverse("tournaments:detail", kwargs={"slug": slug})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, slug)

    def test_apply_get_ok(self):
        response = self.client.get(reverse("tournaments:apply"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ПОДАТИ ЗАЯВКУ")

    def test_archive_ok(self):
        response = self.client.get(reverse("tournaments:archive"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Минулі")
        self.assertContains(response, "Галерея")

    def test_home_archive_link(self):
        response = self.client.get(reverse("tournaments:home"))
        self.assertContains(response, reverse("tournaments:archive"))
