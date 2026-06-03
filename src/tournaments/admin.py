from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    RelatedDropdownFilter,
)

from .models import (
    AgeGroup,
    Application,
    ArchiveEdition,
    GalleryImage,
    Goal,
    Match,
    Player,
    SiteSettings,
    Team,
    Tournament,
)


class TournamentAdminForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = "__all__"
        widgets = {
            "description": TinyMCE(),
        }


class AgeGroupInline(TabularInline):
    model = AgeGroup
    extra = 1
    fields = ("name", "sort_order")
    ordering = ("sort_order",)
    verbose_name = "Вікова група"
    verbose_name_plural = "Вікові групи"


class TeamInline(TabularInline):
    model = Team
    extra = 0
    fields = ("name", "city", "short_code", "wins", "losses", "sort_order")
    ordering = ("sort_order",)
    show_change_link = True
    verbose_name = "Команда"
    verbose_name_plural = "Команди"


class MatchInline(TabularInline):
    model = Match
    extra = 0
    fields = (
        "stage",
        "status",
        "day",
        "time",
        "field",
        "home_team",
        "away_team",
        "age_group",
        "score_home",
        "score_away",
    )
    autocomplete_fields = ("home_team", "away_team", "age_group")
    ordering = ("day", "time")
    verbose_name = "Матч"
    verbose_name_plural = "Матчі"


@admin.register(Tournament)
class TournamentAdmin(ModelAdmin):
    form = TournamentAdminForm
    inlines = (AgeGroupInline, TeamInline, MatchInline)
    list_display = (
        "title",
        "season",
        "year",
        "theme_class",
        "slug",
        "is_published",
        "sort_order",
        "get_hero_image_preview",
    )
    list_filter = (
        ("is_published", ChoicesDropdownFilter),
        ("theme_class", ChoicesDropdownFilter),
        ("season_en", ChoicesDropdownFilter),
    )
    list_editable = ("is_published", "sort_order")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "slug", "subtitle")
    readonly_fields = ("get_hero_image_preview", "get_card_image_preview")
    fieldsets = (
        (
            "Основне",
            {
                "fields": (
                    "slug",
                    "title",
                    "subtitle",
                    "season",
                    "season_en",
                    "year",
                    "theme_class",
                    "is_published",
                    "sort_order",
                ),
            },
        ),
        (
            "Дати та локація",
            {"fields": ("dates_display", "starts_at", "ends_at", "location")},
        ),
        (
            "Формат і статистика",
            {
                "fields": (
                    "match_duration_minutes",
                    "format_text",
                    "teams_count",
                    "matches_count",
                    "goals_count",
                    "wins_count",
                    "losses_count",
                ),
                "description": "Порожні поля голів / перемог / поразок не показуються на сайті.",
            },
        ),
        (
            "Контент",
            {
                "fields": (
                    "description",
                    "highlight",
                    "tagline",
                    "prize",
                    "fee_uah",
                    "age_groups",
                    "icon_hint",
                    "hero_image",
                    "get_hero_image_preview",
                    "card_image",
                    "get_card_image_preview",
                ),
            },
        ),
    )

    @admin.display(description="Hero")
    def get_hero_image_preview(self, obj: Tournament) -> str:
        if obj.hero_image:
            return format_html(
                '<img src="{}" alt="" width="120" height="80">',
                obj.hero_image.url,
            )
        return "—"

    @admin.display(description="Картка")
    def get_card_image_preview(self, obj: Tournament) -> str:
        if obj.card_image:
            return format_html(
                '<img src="{}" alt="" width="120" height="80">',
                obj.card_image.url,
            )
        return "—"


class PlayerInline(TabularInline):
    model = Player
    extra = 0
    fields = ("full_name", "age_group", "sort_order")
    autocomplete_fields = ("age_group",)
    verbose_name = "Гравець"
    verbose_name_plural = "Гравці"


@admin.register(Team)
class TeamAdmin(ModelAdmin):
    list_display = ("name", "short_code", "city", "tournament", "wins", "losses")
    list_filter = (("tournament", RelatedDropdownFilter),)
    search_fields = ("name", "short_code", "city")
    inlines = (PlayerInline,)
    autocomplete_fields = ("tournament",)


@admin.register(Player)
class PlayerAdmin(ModelAdmin):
    list_display = ("full_name", "team", "age_group", "tournament_name")
    list_filter = (("team__tournament", RelatedDropdownFilter), ("age_group", RelatedDropdownFilter))
    search_fields = ("full_name", "team__name")
    autocomplete_fields = ("team", "age_group")

    @admin.display(description="Турнір")
    def tournament_name(self, obj: Player) -> str:
        return str(obj.tournament)


@admin.register(Match)
class MatchAdmin(ModelAdmin):
    list_display = (
        "tournament",
        "home_team",
        "away_team",
        "day",
        "time",
        "stage",
        "status",
        "score_display",
    )
    list_filter = (
        ("tournament", RelatedDropdownFilter),
        ("stage", ChoicesDropdownFilter),
        ("status", ChoicesDropdownFilter),
    )
    search_fields = ("home_team__name", "away_team__name", "field")
    autocomplete_fields = ("tournament", "home_team", "away_team", "age_group")
    inlines: tuple = ()

    @admin.display(description="Рахунок")
    def score_display(self, obj: Match) -> str:
        if obj.score_home is None or obj.score_away is None:
            return "—"
        return f"{obj.score_home}:{obj.score_away}"


class GoalInline(TabularInline):
    model = Goal
    extra = 0
    fields = ("minute", "player", "team")
    autocomplete_fields = ("player", "team")
    verbose_name = "Гол"
    verbose_name_plural = "Голи"


MatchAdmin.inlines = (GoalInline,)


@admin.register(Goal)
class GoalAdmin(ModelAdmin):
    list_display = ("match", "player", "team", "minute", "tournament_name")
    list_filter = (("match__tournament", RelatedDropdownFilter),)
    search_fields = ("player__full_name", "team__name")
    autocomplete_fields = ("match", "player", "team")

    @admin.display(description="Турнір")
    def tournament_name(self, obj: Goal) -> str:
        return str(obj.match.tournament)


@admin.register(AgeGroup)
class AgeGroupAdmin(ModelAdmin):
    list_display = ("name", "tournament", "sort_order")
    list_filter = (("tournament", RelatedDropdownFilter),)
    search_fields = ("name",)
    autocomplete_fields = ("tournament",)


@admin.register(ArchiveEdition)
class ArchiveEditionAdmin(ModelAdmin):
    list_display = ("title", "season", "year", "theme_class", "teams_count", "is_published", "sort_order")
    list_filter = (("theme_class", ChoicesDropdownFilter), ("is_published", ChoicesDropdownFilter))
    list_editable = ("is_published", "sort_order")
    search_fields = ("title", "season", "year")


@admin.register(GalleryImage)
class GalleryImageAdmin(ModelAdmin):
    list_display = (
        "label",
        "get_preview",
        "height",
        "show_on_home",
        "show_on_archive",
        "sort_order",
    )
    list_editable = ("show_on_home", "show_on_archive", "sort_order")
    list_filter = (
        ("show_on_home", ChoicesDropdownFilter),
        ("show_on_archive", ChoicesDropdownFilter),
        ("height", ChoicesDropdownFilter),
    )
    search_fields = ("label", "alt_text")

    @admin.display(description="Превʼю")
    def get_preview(self, obj: GalleryImage) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" alt="" width="80" height="60">',
                obj.image.url,
            )
        return "—"


@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    list_display = (
        "team_name",
        "tournament",
        "phone",
        "email",
        "status",
        "created_at",
    )
    list_filter = (
        ("status", ChoicesDropdownFilter),
        ("tournament", RelatedDropdownFilter),
        "created_at",
    )
    readonly_fields = ("created_at",)
    search_fields = ("team_name", "phone", "email", "coach_name", "city")
    date_hierarchy = "created_at"
    list_select_related = ("tournament",)
    actions = ("mark_processed",)

    @admin.action(description="Позначити як оброблені")
    def mark_processed(self, request, queryset):
        queryset.update(status=Application.Status.PROCESSED)


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    def has_add_permission(self, request) -> bool:
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.objects.first()
        if obj:
            return HttpResponseRedirect(
                reverse("admin:tournaments_sitesettings_change", args=[obj.pk]),
            )
        return super().changelist_view(request, extra_context)
