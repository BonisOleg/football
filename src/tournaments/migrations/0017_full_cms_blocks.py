from django.db import migrations

import re

from src.tournaments.block_defaults import BLOCK_DEFAULTS
from src.tournaments.site_content_registry import BLOCK_FIELD_LABELS, all_registry_block_keys


INLINE_KEY_PATTERN = re.compile(
    r"^(stat_\d+_(value|label|hint)|stat_plus|"
    r"label_dates|label_teams|label_location|label_format|soon_badge|"
    r"hero_btn_detail|hero_btn_apply|hero_btn_soon|hero_swipe_touch|hero_swipe_drag|"
    r"countdown_days|countdown_hours|countdown_mins|countdown_secs)$"
)
MULTILINE_PLAIN_KEYS = frozenset({"marquee", "hero_desc", "stats_aside", "success_desc", "cta_desc"})


def _strip_html(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", text).strip()


def _unwrap_paragraph(value: str) -> str:
    text = (value or "").strip()
    match = re.fullmatch(r"<p>(.*?)</p>", text, flags=re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text


def seed_cms_blocks(apps, schema_editor):
    SiteBlock = apps.get_model("tournaments", "SiteBlock")
    SiteSettings = apps.get_model("tournaments", "SiteSettings")

    for page, key in sorted(all_registry_block_keys()):
        label = BLOCK_FIELD_LABELS.get((page, key), key.replace("_", " ").capitalize())
        default_text = BLOCK_DEFAULTS.get((page, key), "")
        SiteBlock.objects.get_or_create(
            page=page,
            key=key,
            defaults={
                "label": label,
                "content_type": "text",
                "text_html": default_text,
                "sort_order": 0,
                "is_active": True,
            },
        )

    site = SiteSettings.objects.filter(pk=1).first()
    if site:
        about = BLOCK_DEFAULTS.get(("footer", "about"), "")
        copyright_text = BLOCK_DEFAULTS.get(("footer", "copyright"), "")
        cta = BLOCK_DEFAULTS.get(("header", "cta_label"), "")
        updates = {}
        if not site.footer_about and about:
            updates["footer_about"] = about
        if not site.footer_copyright and copyright_text:
            updates["footer_copyright"] = copyright_text
        if not site.header_cta_label and cta:
            updates["header_cta_label"] = cta
        if updates:
            SiteSettings.objects.filter(pk=1).update(**updates)


class Migration(migrations.Migration):

    dependencies = [
        ("tournaments", "0016_strip_inline_block_html"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApplyFormSettings",
            fields=[],
            options={
                "verbose_name": "Форма заявки",
                "verbose_name_plural": "Форма заявки",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.CreateModel(
            name="ApplySuccessSettings",
            fields=[],
            options={
                "verbose_name": "Після заявки",
                "verbose_name_plural": "Після заявки",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.CreateModel(
            name="DetailPageSettings",
            fields=[],
            options={
                "verbose_name": "Сторінка турніру",
                "verbose_name_plural": "Сторінка турніру",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.CreateModel(
            name="HeaderNavigationSettings",
            fields=[],
            options={
                "verbose_name": "Хедер і навігація",
                "verbose_name_plural": "Хедер і навігація",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.CreateModel(
            name="SiteSeoSettings",
            fields=[],
            options={
                "verbose_name": "SEO і заголовки",
                "verbose_name_plural": "SEO і заголовки",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.RunPython(seed_cms_blocks, migrations.RunPython.noop),
    ]
