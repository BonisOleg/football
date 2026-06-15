from django.db import migrations

from src.tournaments.block_defaults import BLOCK_DEFAULTS


LABELS = {
    "archive_btn_all": "Текст кнопки «Дивитись усе»",
    "location_tag": "Мітка локації над hero",
    "label_dates": "Підпис «Дати»",
    "label_teams": "Підпис «Команд»",
    "label_location": "Підпис «Локація»",
    "label_format": "Підпис «Формат»",
    "soon_badge": "Мітка «Скоро»",
    "hero_btn_detail": "Кнопка «Перейти до турніру»",
    "hero_btn_apply": "Кнопка «Подати заявку»",
    "hero_btn_soon": "Кнопка «Скоро» (неактивна)",
    "hero_swipe_touch": "Підказка для мобільних",
    "hero_swipe_drag": "Підказка для десктопу",
    "countdown_days": "Таймер — дні",
    "countdown_hours": "Таймер — години",
    "countdown_mins": "Таймер — хвилини",
    "countdown_secs": "Таймер — секунди",
    "stat_plus": "Знак «+» після цифри",
}


NEW_SITE_BLOCKS = [
    ("home", "archive_btn_all", 22),
    ("home", "location_tag", 23),
    ("home", "label_dates", 24),
    ("home", "label_teams", 25),
    ("home", "label_location", 26),
    ("home", "label_format", 27),
    ("home", "soon_badge", 28),
    ("home", "hero_btn_detail", 29),
    ("home", "hero_btn_apply", 30),
    ("home", "hero_btn_soon", 31),
    ("home", "hero_swipe_touch", 32),
    ("home", "hero_swipe_drag", 33),
    ("home", "countdown_days", 34),
    ("home", "countdown_hours", 35),
    ("home", "countdown_mins", 36),
    ("home", "countdown_secs", 37),
    ("home", "stat_plus", 38),
]


def seed_home_label_blocks(apps, schema_editor):
    SiteBlock = apps.get_model("tournaments", "SiteBlock")
    for page, key, sort_order in NEW_SITE_BLOCKS:
        SiteBlock.objects.update_or_create(
            page=page,
            key=key,
            defaults={
                "label": LABELS.get(key, key),
                "content_type": "text",
                "text_html": BLOCK_DEFAULTS.get((page, key), ""),
                "sort_order": sort_order,
                "is_active": True,
            },
        )


def remove_home_label_blocks(apps, schema_editor):
    SiteBlock = apps.get_model("tournaments", "SiteBlock")
    keys = [key for _page, key, _sort in NEW_SITE_BLOCKS]
    SiteBlock.objects.filter(page="home", key__in=keys).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("tournaments", "0012_sitesettings_season_dates"),
    ]

    operations = [
        migrations.RunPython(seed_home_label_blocks, remove_home_label_blocks),
    ]
