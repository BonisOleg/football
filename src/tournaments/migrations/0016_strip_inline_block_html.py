import re

from django.db import migrations


INLINE_KEY_PATTERN = re.compile(
    r"^(stat_\d+_(value|label|hint)|stat_plus|"
    r"label_dates|label_teams|label_location|label_format|soon_badge|"
    r"hero_btn_detail|hero_btn_apply|hero_btn_soon|hero_swipe_touch|hero_swipe_drag|"
    r"countdown_days|countdown_hours|countdown_mins|countdown_secs)$"
)


def _strip_html(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", text).strip()


def strip_inline_block_html(apps, schema_editor):
    SiteBlock = apps.get_model("tournaments", "SiteBlock")
    for block in SiteBlock.objects.filter(content_type="text"):
        if not INLINE_KEY_PATTERN.match(block.key):
            continue
        cleaned = _strip_html(block.text_html)
        if cleaned != block.text_html:
            block.text_html = cleaned
            block.is_active = True
            block.save(update_fields=["text_html", "is_active"])


class Migration(migrations.Migration):

    dependencies = [
        ("tournaments", "0015_season_archive_admin"),
    ]

    operations = [
        migrations.RunPython(strip_inline_block_html, migrations.RunPython.noop),
    ]
