from pathlib import Path

from decouple import Csv, config
from django.templatetags.static import static
from django.urls import reverse_lazy

from src.tournaments.site_content_registry import (
    build_archive_sidebar_items,
    build_content_sidebar_items,
    build_season_sidebar_items,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "django.contrib.admin",
    "config.auth_config.AuthConfig",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tinymce",
    "django_htmx",
    "src.tournaments",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "config.middleware.AdminUkrainianMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "src.tournaments.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "uk"
LANGUAGES = [
    ("uk", "Українська"),
    ("en", "English"),
]
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@lvivcup.com.ua")
APPLICATION_NOTIFY_EMAIL = config(
    "APPLICATION_NOTIFY_EMAIL",
    default="diegomara@ukr.net",
)

UNFOLD = {
    "SITE_TITLE": "Football Generation",
    "SITE_HEADER": "Адмін-панель",
    "SITE_SUBHEADER": "Керування турнірами та контентом",
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static("images/football-generation-logo.png"),
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "href": lambda request: static("images/favicon.ico"),
            "sizes": "any",
        },
        {
            "rel": "icon",
            "href": lambda request: static("images/favicon-32x32.png"),
            "type": "image/png",
            "sizes": "32x32",
        },
        {
            "rel": "icon",
            "href": lambda request: static("images/favicon-16x16.png"),
            "type": "image/png",
            "sizes": "16x16",
        },
        {
            "rel": "apple-touch-icon",
            "href": lambda request: static("images/apple-touch-icon.png"),
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "COLORS": {
        "primary": {
            "50": "oklch(97% 0.02 85)",
            "100": "oklch(94% 0.04 85)",
            "200": "oklch(91% 0.07 85)",
            "300": "oklch(88% 0.10 85)",
            "400": "oklch(84% 0.14 85)",
            "500": "oklch(78% 0.16 85)",
            "600": "oklch(72% 0.16 85)",
            "700": "oklch(58% 0.14 85)",
            "800": "oklch(46% 0.12 85)",
            "900": "oklch(36% 0.10 85)",
            "950": "oklch(24% 0.08 85)",
        },
    },
    "STYLES": [
        lambda request: static("css/admin/theme.css"),
    ],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Турніри",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Турніри",
                        "icon": "sports_soccer",
                        "link": reverse_lazy("admin:tournaments_tournament_changelist"),
                    },
                    {
                        "title": "Вікові групи",
                        "icon": "groups",
                        "link": reverse_lazy("admin:tournaments_agegroup_changelist"),
                    },
                    {
                        "title": "Команди",
                        "icon": "shield",
                        "link": reverse_lazy("admin:tournaments_team_changelist"),
                    },
                    {
                        "title": "Гравці",
                        "icon": "person",
                        "link": reverse_lazy("admin:tournaments_player_changelist"),
                    },
                    {
                        "title": "Матчі",
                        "icon": "event",
                        "link": reverse_lazy("admin:tournaments_match_changelist"),
                    },
                    {
                        "title": "Голи",
                        "icon": "sports",
                        "link": reverse_lazy("admin:tournaments_goal_changelist"),
                    },
                    {
                        "title": "Заявки",
                        "icon": "assignment",
                        "link": reverse_lazy("admin:tournaments_application_changelist"),
                    },
                    {
                        "title": "Галерея",
                        "icon": "photo_library",
                        "link": reverse_lazy("admin:tournaments_galleryimage_changelist"),
                    },
                ],
            },
            {
                "title": "Контент сайту",
                "collapsible": False,
                "items": [
                    {
                        "title": "Налаштування сайту",
                        "icon": "settings",
                        "link": reverse_lazy("admin:tournaments_sitesettings_changelist"),
                    },
                    *build_content_sidebar_items(),
                ],
            },
            {
                "title": "Сезони",
                "collapsible": False,
                "items": build_season_sidebar_items(),
            },
            {
                "title": "Архів сезонів",
                "collapsible": False,
                "items": [
                    *build_archive_sidebar_items(),
                    {
                        "title": "Архівні турніри",
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:tournaments_archiveedition_changelist"),
                    },
                ],
            },
        ],
    },
    "LOGIN": {
        "form": "src.tournaments.admin_forms.UkrainianAdminAuthenticationForm",
    },
}

TINYMCE_DEFAULT_CONFIG = {
    "height": 360,
    "menubar": False,
    "plugins": "link lists",
    "toolbar": "undo redo | bold italic | bullist numlist | link",
    "skin": "oxide-dark",
    "content_css": "dark",
    "content_style": (
        "body { background: #111827; color: #f9fafb; font-family: inherit; font-size: 14px; }"
    ),
}
