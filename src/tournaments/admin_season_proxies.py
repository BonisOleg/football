from __future__ import annotations

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from unfold.admin import ModelAdmin

from .admin_forms import TournamentAdminForm
from .admin_guidelines import render_admin_warning_callout
from .models import (
    AutumnSeasonTournament,
    KidsSeasonTournament,
    SpringSeasonTournament,
    SummerSeasonTournament,
    Tournament,
    WinterSeasonTournament,
)


class SeasonTournamentAdmin(ModelAdmin):
    """Окрема admin-сторінка на сезон: changelist → change для фіксованого slug."""

    form = TournamentAdminForm
    fixed_slug: str = ""
    inlines = ()
    prepopulated_fields: dict = {}
    readonly_fields = ("content_guidelines", "slug", "get_hero_image_preview", "get_card_image_preview")
    fieldsets = (
        (
            "Увага перед редагуванням",
            {"fields": ("content_guidelines",), "classes": ("wide",)},
        ),
        (
            "Hero на головній",
            {
                "fields": (
                    ("season", "year"),
                    "title",
                    "subtitle",
                    "description",
                    "hero_image",
                    "get_hero_image_preview",
                ),
                "description": (
                    "Тексти та фото hero для цього сезону на головній. "
                    "Hero-зображення використовується як фон блоку."
                ),
            },
        ),
        (
            "Дати та локація",
            {"fields": ("dates_display", "starts_at", "ends_at", "location")},
        ),
        (
            "Картка сезону",
            {
                "fields": (
                    "format_text",
                    "teams_count",
                    "tagline",
                    "card_image",
                    "get_card_image_preview",
                ),
            },
        ),
        (
            "Сторінка турніру",
            {
                "fields": (
                    "slug",
                    "season_en",
                    "theme_class",
                    "match_duration_minutes",
                    "matches_count",
                    "goals_count",
                    "wins_count",
                    "losses_count",
                    "highlight",
                    "prize",
                    "fee_uah",
                    "age_groups",
                    "icon_hint",
                    "is_published",
                    "sort_order",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(slug=self.fixed_slug)

    def changelist_view(self, request, extra_context=None):
        tournament = Tournament.objects.filter(slug=self.fixed_slug).first()
        if tournament:
            return HttpResponseRedirect(
                reverse(
                    f"admin:tournaments_{self.model._meta.model_name}_change",
                    args=[tournament.pk],
                )
            )
        return super().changelist_view(request, extra_context)

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    @admin.display(description="")
    def content_guidelines(self, obj: Tournament) -> str:
        return render_admin_warning_callout("tournament")

    @admin.display(description="Hero")
    def get_hero_image_preview(self, obj: Tournament) -> str:
        from django.utils.html import format_html

        if obj.hero_image:
            return format_html(
                '<img src="{}" alt="" width="120" height="80">',
                obj.hero_image.url,
            )
        return "—"

    @admin.display(description="Картка")
    def get_card_image_preview(self, obj: Tournament) -> str:
        from django.utils.html import format_html

        if obj.card_image:
            return format_html(
                '<img src="{}" alt="" width="120" height="80">',
                obj.card_image.url,
            )
        return "—"


_SEASON_MODELS: tuple[tuple[type[Tournament], str], ...] = (
    (SpringSeasonTournament, "leo-cup"),
    (SummerSeasonTournament, "fg-summer-cup"),
    (AutumnSeasonTournament, "leo-cup-osen"),
    (WinterSeasonTournament, "ruh-cup"),
    (KidsSeasonTournament, "ruh-kids-cup"),
)


def register_season_admins() -> None:
    for model, slug in _SEASON_MODELS:
        class Admin(SeasonTournamentAdmin):
            pass

        Admin.fixed_slug = slug
        admin.site.register(model, Admin)


register_season_admins()
