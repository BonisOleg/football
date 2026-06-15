from django.db import migrations

from src.tournaments.block_defaults import BLOCK_DEFAULTS


TOURNAMENT_REBRAND = {
    "leo-cup": {
        "title": "FG SPRING CUP",
        "prize": "Кубки + медалі + індивідуальні нагороди",
    },
    "leo-cup-osen": {
        "title": "FG AUTUMN CUP",
        "description": (
            "Осіння серія Football Generation — фінальний турнір сезону на природному газоні. "
            "Зустріч найсильніших шкіл Львова, Києва, Тернополя та Івано-Франківська."
        ),
        "prize": "Кубки + медалі + MVP турніру",
    },
    "ruh-cup": {
        "title": "FG CUP",
        "location": "Спортивний манеж, Львів",
        "prize": "Кубок FG + персональні нагороди",
    },
    "ruh-kids-cup": {
        "title": "FG KIDS CUP",
        "location": "Спортивний манеж, Львів",
    },
}

SITE_BLOCKS = [
    ("home", "hero_eyebrow", "Hero — eyebrow", 1),
    ("home", "stats_eyebrow", "Статистика — eyebrow", 2),
    ("home", "stats_title", "Статистика — заголовок", 3),
    ("home", "stats_aside", "Статистика — опис", 4),
    ("home", "calendar_eyebrow", "Календар — eyebrow", 5),
    ("home", "calendar_title", "Календар — заголовок", 6),
    ("home", "archive_eyebrow", "Архів — eyebrow", 7),
    ("home", "archive_title", "Архів — заголовок", 8),
    ("header", "cta_label", "Хедер — кнопка CTA", 1),
    ("footer", "about", "Футер — про організацію", 1),
    ("footer", "copyright", "Футер — copyright", 2),
    ("apply", "hero_eyebrow", "Заявка — eyebrow", 1),
    ("apply", "hero_title", "Заявка — заголовок", 2),
    ("apply", "hero_desc", "Заявка — опис", 3),
    ("archive", "hero_eyebrow", "Архів hero — eyebrow", 1),
    ("archive", "hero_title", "Архів hero — заголовок", 2),
    ("archive", "hero_desc", "Архів hero — опис", 3),
]


def rebrand_forward(apps, schema_editor):
    Tournament = apps.get_model("tournaments", "Tournament")
    ArchiveEdition = apps.get_model("tournaments", "ArchiveEdition")
    SiteSettings = apps.get_model("tournaments", "SiteSettings")
    SiteBlock = apps.get_model("tournaments", "SiteBlock")

    for slug, fields in TOURNAMENT_REBRAND.items():
        Tournament.objects.filter(slug=slug).update(**fields)

    ArchiveEdition.objects.filter(title="LEO CUP", season="Весна").update(title="FG SPRING CUP")
    ArchiveEdition.objects.filter(title="LEO CUP", season="Осінь").update(title="FG AUTUMN CUP")
    ArchiveEdition.objects.filter(title="RUH CUP").update(title="FG CUP")
    ArchiveEdition.objects.filter(title="RUH KIDS CUP").update(title="FG KIDS CUP")

    SiteSettings.objects.filter(pk=1).update(
        site_name="Football Generation",
        header_cta_label="Подати заявку",
        footer_about=BLOCK_DEFAULTS[("footer", "about")],
        footer_copyright=BLOCK_DEFAULTS[("footer", "copyright")],
    )

    for page, key, label, sort_order in SITE_BLOCKS:
        default_text = BLOCK_DEFAULTS.get((page, key), "")
        SiteBlock.objects.update_or_create(
            page=page,
            key=key,
            defaults={
                "label": label,
                "content_type": "text",
                "text_html": default_text,
                "sort_order": sort_order,
                "is_active": True,
            },
        )


def rebrand_backward(apps, schema_editor):
    SiteBlock = apps.get_model("tournaments", "SiteBlock")
    SiteBlock.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("tournaments", "0007_siteblock_and_settings"),
    ]

    operations = [
        migrations.RunPython(rebrand_forward, rebrand_backward),
    ]
