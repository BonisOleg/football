import io

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from src.tournaments.admin_forms import GalleryImageAdminForm, SiteBlockAdminForm, SiteSettingsAdminForm
from src.tournaments.admin_validators import validate_rich_text, validate_video_url
from src.tournaments.models import GalleryImage, SiteBlock, SiteSettings


def make_test_image(
    name: str = "test.jpg",
    size: tuple[int, int] = (800, 600),
    color: str = "red",
    fmt: str = "JPEG",
) -> SimpleUploadedFile:
    buffer = io.BytesIO()
    Image.new("RGB", size, color).save(buffer, format=fmt)
    buffer.seek(0)
    content_type = "image/jpeg" if fmt == "JPEG" else "image/png"
    return SimpleUploadedFile(name, buffer.read(), content_type=content_type)


class RichTextValidatorTests(TestCase):
    def test_rejects_script_tag(self):
        with self.assertRaisesMessage(Exception, "заборонений HTML"):
            validate_rich_text('<p>Hi</p><script>alert(1)</script>', field_key="text_html")

    def test_rejects_img_tag(self):
        with self.assertRaisesMessage(Exception, "заборонений HTML"):
            validate_rich_text('<img src="/x.jpg">', field_key="text_html")

    def test_allows_accent_span_for_title_blocks(self):
        html = 'Минулі<br><span class="text-accent">турніри</span>'
        self.assertEqual(
            validate_rich_text(html, field_key="text_html", allow_accent_span=True),
            html,
        )

    def test_rejects_accent_span_without_permission(self):
        with self.assertRaisesMessage(Exception, "text-accent"):
            validate_rich_text(
                '<span class="text-accent">Accent</span>',
                field_key="text_html",
                allow_accent_span=False,
            )


class VideoValidatorTests(TestCase):
    def test_accepts_youtube_url(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.assertEqual(validate_video_url(url), url)

    def test_rejects_unknown_video_host(self):
        with self.assertRaisesMessage(Exception, "YouTube або Vimeo"):
            validate_video_url("https://example.com/video.mp4")


class SiteBlockAdminFormTests(TestCase):
    def test_rejects_oversized_image(self):
        oversized = make_test_image(size=(800, 600))
        oversized.size = 3 * 1024 * 1024
        form = SiteBlockAdminForm(
            data={
                "page": SiteBlock.Page.HOME,
                "key": "photo",
                "label": "Photo",
                "content_type": SiteBlock.ContentType.IMAGE,
                "text_html": "",
                "video_url": "",
                "sort_order": 0,
                "is_active": True,
            },
            files={"image": oversized},
        )
        self.assertFalse(form.is_valid())
        self.assertIn("image", form.errors)

    def test_rejects_invalid_video_url(self):
        form = SiteBlockAdminForm(
            data={
                "page": SiteBlock.Page.HOME,
                "key": "clip",
                "label": "Clip",
                "content_type": SiteBlock.ContentType.VIDEO,
                "text_html": "",
                "video_url": "https://example.com/video.mp4",
                "sort_order": 0,
                "is_active": True,
            },
        )
        self.assertFalse(form.is_valid())
        self.assertIn("video_url", form.errors)

    def test_allows_hero_title_accent_span(self):
        block = SiteBlock.objects.get(page=SiteBlock.Page.APPLY, key="hero_title")
        form = SiteBlockAdminForm(
            data={
                "page": block.page,
                "key": block.key,
                "label": block.label,
                "content_type": SiteBlock.ContentType.TEXT,
                "text_html": 'Реєструйте<br><span class="text-accent">команду</span>',
                "video_url": "",
                "sort_order": block.sort_order,
                "is_active": block.is_active,
            },
            instance=block,
        )
        self.assertTrue(form.is_valid(), form.errors)


class SiteSettingsAdminFormTests(TestCase):
    def test_rejects_html_in_footer_about(self):
        form = SiteSettingsAdminForm(
            data={
                "site_name": "Football Generation",
                "phone": "+380000000000",
                "email": "test@example.com",
                "city": "Львів",
                "header_cta_label": "Подати заявку",
                "footer_about": "<p>HTML</p>",
                "footer_copyright": "© {year}",
                "url_instagram": "",
                "url_telegram": "",
                "url_youtube": "",
                "url_tiktok": "",
            },
        )
        self.assertFalse(form.is_valid())
        self.assertIn("footer_about", form.errors)


class GalleryImageAdminFormTests(TestCase):
    def test_rejects_narrow_image(self):
        form = GalleryImageAdminForm(
            data={
                "alt_text": "Test",
                "label": "Test",
                "height": GalleryImage.Height.SHORT,
                "sort_order": 0,
                "show_on_home": False,
                "show_on_archive": True,
            },
            files={"image": make_test_image(size=(400, 300))},
        )
        self.assertFalse(form.is_valid())
        self.assertIn("image", form.errors)


@override_settings(ROOT_URLCONF="config.urls")
class AdminWarningUiTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="testpass123",
        )
        self.client.force_login(self.admin_user)
        SiteSettings.load()

    def test_siteblock_change_page_shows_warning_callout(self):
        block = SiteBlock.objects.get(page=SiteBlock.Page.HOME, key="stats_title")
        response = self.client.get(reverse("admin:tournaments_siteblock_change", args=[block.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin-content-warning")
        self.assertContains(response, "можуть зламати вигляд сторінки")

    def test_sitesettings_change_page_shows_warning_callout(self):
        settings_obj = SiteSettings.load()
        response = self.client.get(
            reverse("admin:tournaments_sitesettings_change", args=[settings_obj.pk]),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin-content-warning")

    def test_gallery_change_page_shows_warning_callout(self):
        image = GalleryImage.objects.create(
            image=make_test_image(size=(1200, 800)),
            alt_text="Test",
            label="Test",
        )
        response = self.client.get(reverse("admin:tournaments_galleryimage_change", args=[image.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin-content-warning")
