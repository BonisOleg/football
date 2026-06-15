from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from src.tournaments.models import SiteBlock
from src.tournaments.utils.html import sanitize_html


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tournaments", verbosity=0)

    def test_home_ok(self):
        response = self.client.get(reverse("tournaments:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Football Generation")

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
        for slug in ("leo-cup", "fg-summer-cup", "leo-cup-osen", "ruh-cup", "ruh-kids-cup"):
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

    def test_home_renders_fg_tournament_titles(self):
        response = self.client.get(reverse("tournaments:home"))
        self.assertContains(response, "Football Generation")
        self.assertContains(response, "SPRING")
        self.assertContains(response, "AUTUMN")

    def test_home_starts_with_current_season_tournament(self):
        from datetime import datetime
        from unittest.mock import patch

        from django.utils import timezone

        fixed_now = timezone.make_aware(datetime(2026, 6, 10, 12, 0))
        with patch("django.utils.timezone.now", return_value=fixed_now):
            response = self.client.get(reverse("tournaments:home"))
        self.assertContains(response, 'data-theme="theme-summer"')
        self.assertContains(response, "FG SUMMER CUP")


class HtmlSanitizeTests(TestCase):
    def test_strips_script_tags(self):
        dirty = '<p>Hello</p><script>alert(1)</script>'
        clean = sanitize_html(dirty)
        self.assertNotIn("<script>", clean)
        self.assertIn("<p>Hello</p>", clean)

    def test_allows_basic_formatting(self):
        html = "<p><strong>FG</strong> Cup</p>"
        self.assertEqual(sanitize_html(html), html)

    def test_allows_accent_span(self):
        html = 'Один рік. <span class="text-accent">Пʼять турнірів.</span>'
        self.assertEqual(sanitize_html(html), html)

    def test_strips_span_with_foreign_class(self):
        html = '<span class="danger">Text</span>'
        clean = sanitize_html(html)
        self.assertNotIn("danger", clean)
        self.assertIn("Text", clean)


class SiteBlockTests(TestCase):
    def test_unique_page_key(self):
        SiteBlock.objects.create(
            page=SiteBlock.Page.HOME,
            key="test_key",
            label="Test",
            content_type=SiteBlock.ContentType.TEXT,
            text_html="Test",
        )
        with self.assertRaises(Exception):
            SiteBlock.objects.create(
                page=SiteBlock.Page.HOME,
                key="test_key",
                label="Duplicate",
                content_type=SiteBlock.ContentType.TEXT,
                text_html="Dup",
            )
