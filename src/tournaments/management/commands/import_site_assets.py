"""Download branding and gallery images from lvivcup.com.ua into static/images/."""

from __future__ import annotations

import urllib.request
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

WIX = "https://static.wixstatic.com/media"

BRANDING_ASSETS = {
    "ruh-leo-cup-logo.png": (
        f"{WIX}/7b71cf_50b50bebdb6f4072916a052a12309578~mv2.png"
    ),
}

# Source photos from https://www.lvivcup.com.ua/ (Leo Cup / Ruh Cup pages)
GALLERY_ASSETS = {
    "gallery/opening-ceremony.jpg": (
        f"{WIX}/ae13fd_06320a00f3e8430ab9fdbbb1ba3cc021~mv2.jpg"
        "/v1/fit/w_1200,h_900,al_c,q_85/ae13fd_06320a00f3e8430ab9fdbbb1ba3cc021~mv2.jpg"
    ),
    "gallery/final-match-u12.jpg": (
        f"{WIX}/ae13fd_dd181392e1564229a3dcae83dc58ed50~mv2.jpg"
        "/v1/fit/w_1200,h_900,al_c,q_85/ae13fd_dd181392e1564229a3dcae83dc58ed50~mv2.jpg"
    ),
    "gallery/winner-photo.jpg": (
        f"{WIX}/ae13fd_0bbfc4422c4344ce83b6867d1a4ec5f5~mv2.jpg"
        "/v1/fit/w_1200,h_900,al_c,q_85/ae13fd_0bbfc4422c4344ce83b6867d1a4ec5f5~mv2.jpg"
    ),
    "gallery/crowd-tribunes.jpg": (
        f"{WIX}/ae13fd_a6c18d8e1e5444c7a80d9ccf70d166f7~mv2.jpg"
        "/v1/fit/w_1200,h_900,al_c,q_85/ae13fd_a6c18d8e1e5444c7a80d9ccf70d166f7~mv2.jpg"
    ),
    "gallery/goal-89min.jpg": (
        f"{WIX}/ae13fd_9da455c77aa24d2f821ff2c12b518129~mv2.jpg"
        "/v1/fit/w_1200,h_900,al_c,q_85/ae13fd_9da455c77aa24d2f821ff2c12b518129~mv2.jpg"
    ),
    "gallery/trophy-handover.jpg": (
        f"{WIX}/ae13fd_2e342ce9424f4e35ad160ea165c2870e~mv2.jpg"
        "/v1/fit/w_1200,h_900,al_c,q_85/ae13fd_2e342ce9424f4e35ad160ea165c2870e~mv2.jpg"
    ),
}


class Command(BaseCommand):
    help = (
        "Import static images for RUH LEO CUP site from lvivcup.com.ua. "
        "Для повного імпорту фото та даних використовуйте import_lvivcup."
    )

    def handle(self, *args, **options):
        images_dir = Path(settings.BASE_DIR) / "static" / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        for name, url in {**BRANDING_ASSETS, **GALLERY_ASSETS}.items():
            dest = images_dir / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists() and not options.get("force"):
                self.stdout.write(f"Skip (exists): {name}")
                continue
            try:
                urllib.request.urlretrieve(url, dest)  # noqa: S310
                self.stdout.write(self.style.SUCCESS(f"Saved {name}"))
            except OSError as exc:
                self.stderr.write(f"Failed {name}: {exc}")

        fallback = images_dir / "placeholder.svg"
        if not fallback.exists():
            fallback.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" '
                'viewBox="0 0 400 300"><rect width="400" height="300" fill="#1a1f2e"/>'
                '<text x="200" y="150" fill="#8899aa" text-anchor="middle" '
                'font-family="monospace" font-size="14">RUH LEO CUP</text></svg>',
                encoding="utf-8",
            )
            self.stdout.write(self.style.SUCCESS("Created placeholder.svg"))

        self.stdout.write(self.style.SUCCESS("Asset import finished."))
