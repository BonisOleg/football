from datetime import date

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from src.tournaments.admin_site_content import (
    SEASON_END_FIELD,
    SEASON_START_FIELD,
    block_field_name,
    load_section_blocks,
    _display_plain_text,
    _display_textarea_value,
    _is_inline_field,
    _is_multiline_plain,
    _uses_accent_rich_text,
)
from src.tournaments.context_processors import SITE_BLOCKS_CACHE_KEY
from src.tournaments.models import SiteBlock, SiteSettings
from src.tournaments.site_content_registry import get_section


class SiteContentAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tournaments", verbosity=0)
        call_command("migrate", verbosity=0)
        User = get_user_model()
        cls.user = User.objects.create_superuser(
            username="editor",
            email="editor@example.com",
            password="editor-pass-123",
        )

    def setUp(self):
        self.client.login(username="editor", password="editor-pass-123")
        cache.delete(SITE_BLOCKS_CACHE_KEY)

    def test_legacy_page_url_redirects_to_hero_proxy(self):
        url = reverse("admin:tournaments_siteblock_page", args=["home"])
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse("admin:tournaments_homeherosettings_change", args=[1]),
        )

    def test_home_hero_section_get(self):
        url = reverse("admin:tournaments_homeherosettings_change", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Головний банер")
        self.assertContains(response, "Текст у зеленій мітці")
        self.assertContains(response, "Початок сезону")
        self.assertNotContains(response, "id_block__home__marquee__text_html")
        self.assertNotContains(response, "__is_active")
        self.assertNotContains(response, "показувати на сайті")
        self.assertNotContains(response, "tox-tinymce")
        self.assertNotContains(response, "tinyMCE")

    def test_admin_sidebar_lists_content_sections(self):
        response = self.client.get(reverse("admin:tournaments_homeherosettings_change", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Налаштування сайту")
        self.assertContains(response, "Головний банер")
        self.assertContains(response, "Секція «Один рік 4 турніри»")
        self.assertContains(response, "Секція «Календар сезону»")
        self.assertContains(response, "Хедер і навігація")
        self.assertContains(response, "Форма заявки")
        self.assertContains(response, "Після заявки")
        self.assertContains(response, "Сторінка турніру")
        self.assertContains(response, "SEO і заголовки")
        self.assertNotContains(response, "Турніри та дані")
        self.assertNotContains(response, "Показник 1")
        self.assertNotContains(response, "Головна ·")

    def test_apply_form_section_get(self):
        url = reverse("admin:tournaments_applyformsettings_change", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Форма заявки")
        self.assertContains(response, "id_block__apply__field_team_name_label__text_html")

    def test_header_navigation_section_get(self):
        url = reverse("admin:tournaments_headernavigationsettings_change", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Хедер і навігація")
        self.assertContains(response, "id_block__header__nav_home__text_html")

    def test_detail_page_section_get(self):
        url = reverse("admin:tournaments_detailpagesettings_change", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Сторінка турніру")
        self.assertContains(response, "id_block__detail__bracket_title__text_html")

    def test_footer_section_includes_about_and_columns(self):
        url = reverse("admin:tournaments_footersettings_change", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "id_block__footer__about__text_html")
        self.assertContains(response, "id_block__footer__col_tournaments__text_html")

    def test_home_renders_editable_card_labels(self):
        SiteBlock.objects.filter(page="home", key="label_dates").update(
            text_html="ДАТИ ТЕСТ",
            is_active=True,
        )
        cache.delete(SITE_BLOCKS_CACHE_KEY)

        response = self.client.get(reverse("tournaments:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ДАТИ ТЕСТ")

    def test_marquee_section_is_separate_page(self):
        url = reverse("admin:tournaments_homemarqueesettings_change", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Бігучий рядок")
        self.assertNotContains(response, "Початок сезону")

    def test_season_stats_section_contains_all_indicators(self):
        url = reverse("admin:tournaments_homeseasonstatssettings_change", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Секція «Один рік 4 турніри»")
        self.assertContains(response, "Показник 1")
        self.assertContains(response, "Показник 4")
        self.assertContains(response, "id_block__home__stat_1_value__text_html")
        self.assertContains(response, "id_block__home__stat_4_hint__text_html")
        self.assertNotContains(response, "id_block__home__stat_1_value__is_active")
        self.assertNotContains(response, "stat_1_value__is_active")
        self.assertNotContains(response, "tox-tinymce")
        self.assertContains(response, "site-content-editor__inline-input")

    def test_legacy_stat_section_redirects_to_season_stats(self):
        url = reverse("admin:tournaments_siteblock_section", args=["home", "stat-1"])
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse("admin:tournaments_homeseasonstatssettings_change", args=[1]),
        )

    def test_apply_aside_section_get(self):
        url = reverse("admin:tournaments_applyasidesettings_change", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Секція «Контакти заявки»")
        self.assertContains(response, "Телефон")
        self.assertContains(response, "Email")

    def test_proxy_changelist_redirects_to_change_form(self):
        url = reverse("admin:tournaments_homemarqueesettings_changelist")
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse("admin:tournaments_homemarqueesettings_change", args=[1]),
        )

    def test_changelist_redirects_to_home_hero(self):
        url = reverse("admin:tournaments_siteblock_changelist")
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse("admin:tournaments_homeherosettings_change", args=[1]),
        )

    def test_marquee_post_saves_block_and_clears_cache(self):
        block = SiteBlock.objects.get(page="home", key="marquee")
        block.text_html = "OLD VALUE"
        block.save()
        cache.set(SITE_BLOCKS_CACHE_KEY, {"home.marquee": block}, 60)

        url = reverse("admin:tournaments_homemarqueesettings_change", args=[1])
        post_data = self._section_form_payload("home", "marquee", marquee="НОВИЙ СКРОЛ\nДРУГИЙ РЯДОК")
        response = self.client.post(url, post_data)
        self.assertRedirects(response, url)

        block.refresh_from_db()
        self.assertIn("НОВИЙ СКРОЛ", block.text_html)

        from src.tournaments.context_processors import _load_site_blocks

        cached = _load_site_blocks()
        self.assertIn("НОВИЙ СКРОЛ", cached["home.marquee"].text_html)

    def test_season_stats_post_saves_all_indicators(self):
        url = reverse("admin:tournaments_homeseasonstatssettings_change", args=[1])
        post_data = self._section_form_payload(
            "home",
            "season-stats",
            stat_1_value="111",
            stat_2_value="222",
            stat_3_value="333",
            stat_4_value="444",
        )
        response = self.client.post(url, post_data)
        self.assertRedirects(response, url)

        self.assertEqual(
            SiteBlock.objects.get(page="home", key="stat_1_value").text_html,
            "111",
        )
        self.assertEqual(
            SiteBlock.objects.get(page="home", key="stat_4_value").text_html,
            "444",
        )

    def test_hero_post_saves_season_dates(self):
        url = reverse("admin:tournaments_homeherosettings_change", args=[1])
        post_data = self._section_form_payload(
            "home",
            "hero",
            hero_eyebrow="Сезон {season_start} — {season_end}",
        )
        post_data[SEASON_START_FIELD] = "2026-03-01"
        post_data[SEASON_END_FIELD] = "2026-11-30"
        response = self.client.post(url, post_data)
        self.assertRedirects(response, url)

        settings_obj = SiteSettings.load()
        self.assertEqual(settings_obj.season_start, date(2026, 3, 1))
        self.assertEqual(settings_obj.season_end, date(2026, 11, 30))

    def test_footer_post_syncs_site_settings(self):
        url = reverse("admin:tournaments_footersettings_change", args=[1])
        post_data = self._section_form_payload(
            "footer",
            "copyright",
            about="Новий текст про організацію",
            copyright="© {year} Test Org",
        )
        response = self.client.post(url, post_data)
        self.assertRedirects(response, url)

        settings_obj = SiteSettings.load()
        self.assertEqual(settings_obj.footer_about, "Новий текст про організацію")
        self.assertEqual(settings_obj.footer_copyright, "© {year} Test Org")

    def test_header_post_syncs_cta_label(self):
        url = reverse("admin:tournaments_headernavigationsettings_change", args=[1])
        post_data = self._section_form_payload(
            "header",
            "navigation",
            cta_label="Записатися",
        )
        response = self.client.post(url, post_data)
        self.assertRedirects(response, url)

        settings_obj = SiteSettings.load()
        self.assertEqual(settings_obj.header_cta_label, "Записатися")

    def _section_form_payload(self, page_slug: str, section_slug: str, **overrides):
        section = get_section(page_slug, section_slug)
        blocks = load_section_blocks(section)
        payload: dict[str, str] = {}

        if "contact_info" in section.extra_fields:
            payload["contact_phone"] = overrides.pop("contact_phone", "+38 000 000 00 00")
            payload["contact_email"] = overrides.pop("contact_email", "test@example.com")

        if "season_dates" in section.extra_fields:
            payload[SEASON_START_FIELD] = overrides.pop("season_start", "")
            payload[SEASON_END_FIELD] = overrides.pop("season_end", "")

        for block in blocks.values():
            page = block.page
            key = block.key
            if block.content_type == SiteBlock.ContentType.TEXT:
                raw = overrides.get(key, block.text_html or f"value-{key}")
                if _is_inline_field(key):
                    raw = _display_plain_text(raw)
                elif _uses_accent_rich_text(key):
                    raw = overrides.get(key, block.text_html or f"value-{key}")
                elif _is_multiline_plain(key):
                    raw = _display_textarea_value(raw)
                else:
                    raw = _display_textarea_value(raw)
                payload[block_field_name(page, key, "text_html")] = raw

        for key, value in overrides.items():
            if key.startswith("block__"):
                payload[key] = value
            elif key in {"marquee", "hero_eyebrow"}:
                payload[block_field_name("home", key, "text_html")] = value

        return payload

    def test_admin_sidebar_lists_seasons_and_archive_groups(self):
        response = self.client.get(reverse("admin:tournaments_homeherosettings_change", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Сезони")
        self.assertContains(response, "Сезон «Літо»")
        self.assertContains(response, "Архів сезонів")
        self.assertContains(response, "Секція «Результати за роки»")
        self.assertContains(response, "Секція «Галерея архіву»")
        self.assertNotContains(response, "Секція «Банер архіву»")

    def test_summer_season_changelist_redirects_to_change_form(self):
        from src.tournaments.models import Tournament

        tournament = Tournament.objects.get(slug="fg-summer-cup")
        url = reverse("admin:tournaments_summerseasontournament_changelist")
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse("admin:tournaments_summerseasontournament_change", args=[tournament.pk]),
        )

    def test_summer_season_admin_shows_hero_fields(self):
        from src.tournaments.models import Tournament

        tournament = Tournament.objects.get(slug="fg-summer-cup")
        url = reverse("admin:tournaments_summerseasontournament_change", args=[tournament.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hero на головній")
        self.assertContains(response, "id_hero_image")

    def test_archive_editions_section_get(self):
        url = reverse("admin:tournaments_archiveeditionssectionsettings_change", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Секція «Результати за роки»")
        self.assertContains(response, "id_block__archive__label_teams__text_html")


class HomeBlockContentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tournaments", verbosity=0)
        call_command("migrate", verbosity=0)

    def setUp(self):
        cache.delete(SITE_BLOCKS_CACHE_KEY)

    def test_home_renders_marquee_from_site_block(self):
        SiteBlock.objects.filter(page="home", key="marquee").update(
            text_html="ТЕСТОВИЙ MARQUEE\nЩЕ ОДИН РЯДОК",
            is_active=True,
        )
        cache.delete(SITE_BLOCKS_CACHE_KEY)

        response = self.client.get(reverse("tournaments:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ТЕСТОВИЙ MARQUEE")
        self.assertContains(response, "ЩЕ ОДИН РЯДОК")

    def test_home_renders_stats_from_site_block(self):
        SiteBlock.objects.filter(page="home", key="stat_1_value").update(
            text_html="999",
            is_active=True,
        )
        SiteBlock.objects.filter(page="home", key="stat_1_label").update(
            text_html="Тестовий показник",
            is_active=True,
        )
        cache.delete(SITE_BLOCKS_CACHE_KEY)

        response = self.client.get(reverse("tournaments:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-value="999"')
        self.assertContains(response, "Тестовий показник")

    def test_home_renders_season_placeholders_in_hero_eyebrow(self):
        settings_obj = SiteSettings.load()
        settings_obj.season_start = date(2026, 3, 12)
        settings_obj.season_end = date(2026, 11, 20)
        settings_obj.save(update_fields=["season_start", "season_end"])

        SiteBlock.objects.filter(page="home", key="hero_eyebrow").update(
            text_html="Сезон {season_start} — {season_end}",
            is_active=True,
        )
        cache.delete(SITE_BLOCKS_CACHE_KEY)

        response = self.client.get(reverse("tournaments:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "12 березня 2026")
        self.assertContains(response, "20 листопада 2026")

    def test_archive_page_renders_editable_section_labels(self):
        SiteBlock.objects.filter(page="archive", key="editions_eyebrow").update(
            text_html="АРХІВ ТЕСТ",
            is_active=True,
        )
        cache.delete(SITE_BLOCKS_CACHE_KEY)

        response = self.client.get(reverse("tournaments:archive"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "АРХІВ ТЕСТ")
