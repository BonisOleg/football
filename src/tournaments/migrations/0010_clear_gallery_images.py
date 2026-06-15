from django.db import migrations


def clear_gallery_images(apps, schema_editor):
    GalleryImage = apps.get_model("tournaments", "GalleryImage")
    GalleryImage.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("tournaments", "0009_summer_season"),
    ]

    operations = [
        migrations.RunPython(clear_gallery_images, migrations.RunPython.noop),
    ]
