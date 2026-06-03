from django.db import migrations

HOME_GALLERY_TEASER_LIMIT = 6


def enable_home_gallery_teaser(apps, schema_editor):
    GalleryImage = apps.get_model("tournaments", "GalleryImage")
    home_ids = list(
        GalleryImage.objects.order_by("sort_order", "pk").values_list("pk", flat=True)[
            :HOME_GALLERY_TEASER_LIMIT
        ]
    )
    if not home_ids:
        return
    GalleryImage.objects.filter(pk__in=home_ids).update(show_on_home=True)


class Migration(migrations.Migration):

    dependencies = [
        ("tournaments", "0005_seed_archive_editions"),
    ]

    operations = [
        migrations.RunPython(enable_home_gallery_teaser, migrations.RunPython.noop),
    ]
