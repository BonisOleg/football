from django.db import migrations

from src.tournaments.block_defaults import BLOCK_DEFAULTS


ARCHIVE_BLOCKS = [
    ("archive", "editions_eyebrow", "Архів — eyebrow секції результатів", 4),
    ("archive", "editions_title", "Архів — заголовок секції результатів", 5),
    ("archive", "label_teams", "Архів — підпис «Команд»", 6),
    ("archive", "label_matches", "Архів — підпис «Матчів»", 7),
    ("archive", "label_goals", "Архів — підпис «Голів»", 8),
    ("archive", "gallery_eyebrow", "Архів — eyebrow галереї", 9),
    ("archive", "gallery_title", "Архів — заголовок галереї", 10),
]


def seed_archive_blocks(apps, schema_editor):
    SiteBlock = apps.get_model("tournaments", "SiteBlock")
    for page, key, label, sort_order in ARCHIVE_BLOCKS:
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


def unseed_archive_blocks(apps, schema_editor):
    SiteBlock = apps.get_model("tournaments", "SiteBlock")
    keys = [key for _page, key, _label, _order in ARCHIVE_BLOCKS]
    SiteBlock.objects.filter(page="archive", key__in=keys).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("tournaments", "0014_site_content_proxy_models"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArchiveEditionsSectionSettings",
            fields=[],
            options={
                "verbose_name": "Секція «Результати за роки»",
                "verbose_name_plural": "Секція «Результати за роки»",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.CreateModel(
            name="ArchiveGallerySectionSettings",
            fields=[],
            options={
                "verbose_name": "Секція «Галерея архіву»",
                "verbose_name_plural": "Секція «Галерея архіву»",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.CreateModel(
            name="SpringSeasonTournament",
            fields=[],
            options={
                "verbose_name": "Сезон «Весна»",
                "verbose_name_plural": "Сезон «Весна»",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.tournament",),
        ),
        migrations.CreateModel(
            name="SummerSeasonTournament",
            fields=[],
            options={
                "verbose_name": "Сезон «Літо»",
                "verbose_name_plural": "Сезон «Літо»",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.tournament",),
        ),
        migrations.CreateModel(
            name="AutumnSeasonTournament",
            fields=[],
            options={
                "verbose_name": "Сезон «Осінь»",
                "verbose_name_plural": "Сезон «Осінь»",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.tournament",),
        ),
        migrations.CreateModel(
            name="WinterSeasonTournament",
            fields=[],
            options={
                "verbose_name": "Сезон «Зима»",
                "verbose_name_plural": "Сезон «Зима»",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.tournament",),
        ),
        migrations.CreateModel(
            name="KidsSeasonTournament",
            fields=[],
            options={
                "verbose_name": "Сезон «Kids»",
                "verbose_name_plural": "Сезон «Kids»",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.tournament",),
        ),
        migrations.RunPython(seed_archive_blocks, unseed_archive_blocks),
    ]
