from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from src.tournaments.context_processors import SITE_BLOCKS_CACHE_KEY
from src.tournaments.forms import ApplicationForm
from src.tournaments.models import SiteBlock, Tournament
from src.tournaments.site_content_registry import all_registry_block_keys


class SiteBlockCoverageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tournaments", verbosity=0)
        call_command("migrate", verbosity=0)

    def setUp(self):
        cache.delete(SITE_BLOCKS_CACHE_KEY)

    def test_all_registry_blocks_exist_in_database(self):
        for page, key in all_registry_block_keys():
            self.assertTrue(
                SiteBlock.objects.filter(page=page, key=key).exists(),
                msg=f"Missing block {page}.{key}",
            )

    def test_apply_form_uses_block_labels(self):
        SiteBlock.objects.filter(page="apply", key="field_team_name_label").update(
            text_html="Тестова назва",
            is_active=True,
        )
        cache.delete(SITE_BLOCKS_CACHE_KEY)

        form = ApplicationForm()
        self.assertEqual(form.fields["team_name"].label, "Тестова назва")

    def test_apply_page_renders_form_blocks(self):
        SiteBlock.objects.filter(page="apply", key="form_team_title").update(
            text_html="Тестові дані",
            is_active=True,
        )
        cache.delete(SITE_BLOCKS_CACHE_KEY)

        response = self.client.get(reverse("tournaments:apply"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестові дані")

    def test_header_renders_navigation_blocks(self):
        SiteBlock.objects.filter(page="header", key="nav_home").update(
            text_html="Головна тест",
            is_active=True,
        )
        cache.delete(SITE_BLOCKS_CACHE_KEY)

        response = self.client.get(reverse("tournaments:home"))
        self.assertContains(response, "Головна тест")

    def test_detail_page_renders_section_blocks(self):
        tournament = Tournament.objects.filter(is_published=True).first()
        SiteBlock.objects.filter(page="detail", key="bracket_title").update(
            text_html="Тестова сітка",
            is_active=True,
        )
        cache.delete(SITE_BLOCKS_CACHE_KEY)

        response = self.client.get(tournament.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестова сітка")

    def test_footer_renders_tagline_block(self):
        SiteBlock.objects.filter(page="footer", key="tagline").update(
            text_html="ТЕСТ TAGLINE",
            is_active=True,
        )
        cache.delete(SITE_BLOCKS_CACHE_KEY)

        response = self.client.get(reverse("tournaments:home"))
        self.assertContains(response, "ТЕСТ TAGLINE")

    def test_seo_page_title_from_block(self):
        SiteBlock.objects.filter(page="site", key="apply_page_title").update(
            text_html="Заявка тест title",
            is_active=True,
        )
        cache.delete(SITE_BLOCKS_CACHE_KEY)

        response = self.client.get(reverse("tournaments:apply"))
        self.assertContains(response, "<title>Заявка тест title</title>")
