from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tournaments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="tournament",
            name="ends_at",
            field=models.DateTimeField(
                blank=True,
                help_text="Після цієї дати таймер зворотного відліку не показується.",
                null=True,
                verbose_name="Завершення",
            ),
        ),
        migrations.AddField(
            model_name="tournament",
            name="wins_count",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Залиште порожнім, щоб приховати на сайті до внесення результатів.",
                null=True,
                verbose_name="Перемог",
            ),
        ),
        migrations.AlterField(
            model_name="tournament",
            name="goals_count",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Залиште порожнім, щоб приховати на сайті до внесення результатів.",
                null=True,
                verbose_name="Голів",
            ),
        ),
    ]
