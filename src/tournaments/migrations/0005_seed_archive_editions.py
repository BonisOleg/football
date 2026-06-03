from django.db import migrations


def seed_archive_editions(apps, schema_editor):
    ArchiveEdition = apps.get_model("tournaments", "ArchiveEdition")
    if ArchiveEdition.objects.exists():
        return

    rows = [
        {
            "year": "2025",
            "title": "LEO CUP",
            "season": "Весна",
            "teams_count": 58,
            "matches_count": 72,
            "goals_count": 312,
            "theme_class": "theme-spring",
            "sort_order": 1,
        },
        {
            "year": "2025",
            "title": "LEO CUP",
            "season": "Осінь",
            "teams_count": 44,
            "matches_count": 56,
            "goals_count": 248,
            "theme_class": "theme-autumn",
            "sort_order": 2,
        },
        {
            "year": "2025",
            "title": "RUH CUP",
            "season": "Зима",
            "teams_count": 36,
            "matches_count": 48,
            "goals_count": 196,
            "theme_class": "theme-winter",
            "sort_order": 3,
        },
        {
            "year": "2024",
            "title": "RUH KIDS CUP",
            "season": "Kids",
            "teams_count": 52,
            "matches_count": 64,
            "goals_count": 284,
            "theme_class": "theme-kids",
            "sort_order": 4,
        },
    ]
    for row in rows:
        ArchiveEdition.objects.create(**row)


class Migration(migrations.Migration):
    dependencies = [
        ("tournaments", "0004_tournament_content_and_archive"),
    ]

    operations = [
        migrations.RunPython(seed_archive_editions, migrations.RunPython.noop),
    ]
