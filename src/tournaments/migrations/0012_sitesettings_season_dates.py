from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tournaments", "0011_home_marquee_stats_blocks"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="season_end",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name="Кінець сезону",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="season_start",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name="Початок сезону",
            ),
        ),
    ]
