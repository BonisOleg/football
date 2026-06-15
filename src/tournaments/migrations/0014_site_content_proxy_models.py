from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tournaments", "0013_home_ui_label_blocks"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApplyAsideSettings",
            fields=[],
            options={
                "verbose_name": "Секція «Контакти заявки»",
                "verbose_name_plural": "Секція «Контакти заявки»",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.CreateModel(
            name="ApplyHeroSettings",
            fields=[],
            options={
                "verbose_name": "Секція «Банер заявки»",
                "verbose_name_plural": "Секція «Банер заявки»",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.CreateModel(
            name="ArchiveHeroSettings",
            fields=[],
            options={
                "verbose_name": "Секція «Банер архіву»",
                "verbose_name_plural": "Секція «Банер архіву»",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.CreateModel(
            name="FooterSettings",
            fields=[],
            options={
                "verbose_name": "Футер",
                "verbose_name_plural": "Футер",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.CreateModel(
            name="HomeArchiveTeaserSettings",
            fields=[],
            options={
                "verbose_name": "Секція «Архів на головній»",
                "verbose_name_plural": "Секція «Архів на головній»",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.CreateModel(
            name="HomeCalendarSettings",
            fields=[],
            options={
                "verbose_name": "Секція «Календар сезону»",
                "verbose_name_plural": "Секція «Календар сезону»",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.CreateModel(
            name="HomeHeroSettings",
            fields=[],
            options={
                "verbose_name": "Головний банер",
                "verbose_name_plural": "Головний банер",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.CreateModel(
            name="HomeMarqueeSettings",
            fields=[],
            options={
                "verbose_name": "Бігучий рядок",
                "verbose_name_plural": "Бігучий рядок",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
        migrations.CreateModel(
            name="HomeSeasonStatsSettings",
            fields=[],
            options={
                "verbose_name": "Секція «Один рік 4 турніри»",
                "verbose_name_plural": "Секція «Один рік 4 турніри»",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("tournaments.sitesettings",),
        ),
    ]
