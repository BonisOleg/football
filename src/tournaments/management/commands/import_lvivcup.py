"""Import photos and tournament data from https://www.lvivcup.com.ua/."""

from django.core.management.base import BaseCommand

from src.tournaments.lvivcup_import import LvivcupImporter, discover_live_links


class Command(BaseCommand):
    help = (
        "Завантажує фото з lvivcup.com.ua та імпортує команди, гравців, "
        "матчі й статистику з Tournify (Firestore)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--images-only",
            action="store_true",
            help="Лише завантажити зображення з Wix",
        )
        parser.add_argument(
            "--data-only",
            action="store_true",
            help="Лише імпорт турнірних даних (без фото)",
        )
        parser.add_argument(
            "--force-images",
            action="store_true",
            help="Перезавантажити зображення, навіть якщо вони вже є",
        )
        parser.add_argument(
            "--live-link",
            action="append",
            dest="live_links",
            help="Імпортувати лише вказаний Tournify slug (можна кілька разів)",
        )
        parser.add_argument(
            "--list-links",
            action="store_true",
            help="Показати знайдені Tournify slug і вийти",
        )

    def handle(self, *args, **options):
        if options["list_links"]:
            links = sorted(discover_live_links())
            self.stdout.write(f"Знайдено {len(links)} slug:")
            for link in links:
                self.stdout.write(f"  · {link}")
            return

        importer = LvivcupImporter(stdout=self.stdout, stderr=self.stderr)
        import_images = not options["data_only"]
        import_data = not options["images_only"]

        if options["live_links"]:
            if import_images:
                importer.import_images(force=options["force_images"])
            for live_link in options["live_links"]:
                importer.import_live_link(live_link)
        else:
            importer.import_all(
                images=import_images,
                tournaments=import_data,
                force_images=options["force_images"],
            )

        stats = importer.stats
        self.stdout.write(
            self.style.SUCCESS(
                "Готово: "
                f"фото {stats.images_downloaded}, галерея {stats.gallery_created}, "
                f"команд +{stats.teams_created}/~{stats.teams_updated}, "
                f"гравців +{stats.players_created}/~{stats.players_updated}, "
                f"матчів +{stats.matches_created}/~{stats.matches_updated}"
            )
        )
