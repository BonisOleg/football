from __future__ import annotations

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from unfold.admin import ModelAdmin

from .admin_site_content import site_content_section_view
from .models import (
    ApplyAsideSettings,
    ApplyFormSettings,
    ApplyHeroSettings,
    ApplySuccessSettings,
    ArchiveEditionsSectionSettings,
    ArchiveGallerySectionSettings,
    ArchiveHeroSettings,
    DetailPageSettings,
    FooterSettings,
    HeaderNavigationSettings,
    HomeArchiveTeaserSettings,
    HomeCalendarSettings,
    HomeHeroSettings,
    HomeMarqueeSettings,
    HomeSeasonStatsSettings,
    SiteSeoSettings,
    SiteSettings,
)


class SingletonSettingsAdmin(ModelAdmin):
    """Один запис (pk=1); changelist одразу відкриває форму редагування."""

    def has_add_permission(self, request) -> bool:
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        url_name = f"admin:tournaments_{self.model._meta.model_name}_change"
        return HttpResponseRedirect(reverse(url_name, args=[obj.pk]))


class SiteContentSectionAdmin(SingletonSettingsAdmin):
    page_slug: str = ""
    section_slug: str = ""

    def change_view(self, request, object_id, form_url="", extra_context=None):
        return site_content_section_view(
            request,
            self.page_slug,
            self.section_slug,
            model_admin=self,
        )


_SECTION_MODELS: tuple[tuple[type[SiteSettings], str, str], ...] = (
    (HomeHeroSettings, "home", "hero"),
    (HomeMarqueeSettings, "home", "marquee"),
    (HomeSeasonStatsSettings, "home", "season-stats"),
    (HomeCalendarSettings, "home", "calendar"),
    (HomeArchiveTeaserSettings, "home", "archive-teaser"),
    (HeaderNavigationSettings, "header", "navigation"),
    (ApplyHeroSettings, "apply", "hero"),
    (ApplyFormSettings, "apply", "form"),
    (ApplyAsideSettings, "apply", "aside"),
    (ApplySuccessSettings, "apply", "success"),
    (DetailPageSettings, "detail", "page"),
    (ArchiveHeroSettings, "archive", "hero"),
    (ArchiveEditionsSectionSettings, "archive", "editions"),
    (ArchiveGallerySectionSettings, "archive", "gallery"),
    (FooterSettings, "footer", "copyright"),
    (SiteSeoSettings, "site", "seo"),
)


def register_site_content_section_admins() -> None:
    for model, page_slug, section_slug in _SECTION_MODELS:
        class SectionAdmin(SiteContentSectionAdmin):
            pass

        SectionAdmin.page_slug = page_slug
        SectionAdmin.section_slug = section_slug
        admin.site.register(model, SectionAdmin)


register_site_content_section_admins()
