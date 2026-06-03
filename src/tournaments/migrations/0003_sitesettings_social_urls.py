from django.db import migrations

SOCIAL_URLS = {
    "url_instagram": "https://www.instagram.com/ruh_leo_cup/",
    "url_telegram": "https://t.me/+Vb_0wcwhc4-Foxg5",
    "url_youtube": "https://www.youtube.com/@RUHCUP",
    "url_tiktok": "https://www.tiktok.com/@ruh_leo_cup",
}

PLACEHOLDER_URLS = {
    "url_instagram": "https://www.instagram.com/",
    "url_telegram": "https://t.me/",
    "url_youtube": "https://www.youtube.com/",
    "url_tiktok": "https://www.tiktok.com/",
}


def set_social_urls(apps, schema_editor):
    SiteSettings = apps.get_model("tournaments", "SiteSettings")
    for settings in SiteSettings.objects.all():
        updates = {}
        for field, url in SOCIAL_URLS.items():
            current = getattr(settings, field, "") or ""
            if not current or current in PLACEHOLDER_URLS.values():
                updates[field] = url
        if updates:
            SiteSettings.objects.filter(pk=settings.pk).update(**updates)


class Migration(migrations.Migration):

    dependencies = [
        ("tournaments", "0002_tournament_ends_at_nullable_stats"),
    ]

    operations = [
        migrations.RunPython(set_social_urls, migrations.RunPython.noop),
    ]
