from django.db import migrations

from src.tournaments.block_defaults import BLOCK_DEFAULTS


NEW_SITE_BLOCKS = [
    ("home", "marquee", "Скрол — пункти бігучого рядка", 9),
    ("home", "stat_1_value", "Цифра 1 — значення", 10),
    ("home", "stat_1_label", "Цифра 1 — підпис", 11),
    ("home", "stat_1_hint", "Цифра 1 — підказка", 12),
    ("home", "stat_2_value", "Цифра 2 — значення", 13),
    ("home", "stat_2_label", "Цифра 2 — підпис", 14),
    ("home", "stat_2_hint", "Цифра 2 — підказка", 15),
    ("home", "stat_3_value", "Цифра 3 — значення", 16),
    ("home", "stat_3_label", "Цифра 3 — підпис", 17),
    ("home", "stat_3_hint", "Цифра 3 — підказка", 18),
    ("home", "stat_4_value", "Цифра 4 — значення", 19),
    ("home", "stat_4_label", "Цифра 4 — підпис", 20),
    ("home", "stat_4_hint", "Цифра 4 — підказка", 21),
]


def seed_home_blocks(apps, schema_editor):
    SiteBlock = apps.get_model("tournaments", "SiteBlock")
    for page, key, label, sort_order in NEW_SITE_BLOCKS:
        SiteBlock.objects.update_or_create(
            page=page,
            key=key,
            defaults={
                "label": label,
                "content_type": "text",
                "text_html": BLOCK_DEFAULTS.get((page, key), ""),
                "sort_order": sort_order,
                "is_active": True,
            },
        )


def remove_home_blocks(apps, schema_editor):
    SiteBlock = apps.get_model("tournaments", "SiteBlock")
    keys = [key for _page, key, _label, _sort in NEW_SITE_BLOCKS]
    SiteBlock.objects.filter(page="home", key__in=keys).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("tournaments", "0010_clear_gallery_images"),
    ]

    operations = [
        migrations.RunPython(seed_home_blocks, remove_home_blocks),
    ]
