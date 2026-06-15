from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, TemplateView

from .forms import ApplicationForm
from .mock_data import (
    ARCHIVE_EDITIONS,
    ARCHIVE_GALLERY,
    BRACKET_MOCK,
    GALLERY_TEASER,
    SCHEDULE_MOCK,
    TEAMS_POOL,
    TOP_SCORERS,
)
from .models import Application, ArchiveEdition, Tournament
from .season_timeline import (
    find_wheel_slot,
    get_calendar_season_slots,
    get_home_season_timeline,
    presentation_from_db,
)
from .context_processors import _load_site_blocks
from .services import (
    get_archive_gallery,
    get_bracket,
    get_gallery_teaser,
    get_apply_tournaments,
    get_published_tournaments,
    tournament_is_open_for_apply,
    get_schedule,
    get_teams_pool,
    get_top_scorers,
)
from .utils.site_blocks_data import get_hub_stats, get_marquee_items


class HomeView(TemplateView):
    template_name = "tournaments/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        wheel_slots, active_wheel_index = get_home_season_timeline()
        active_slot = wheel_slots[active_wheel_index] if wheel_slots else None
        calendar_slots = get_calendar_season_slots(wheel_slots)
        gallery = get_gallery_teaser()
        site_blocks = _load_site_blocks()
        ctx.update(
            {
                "wheel_slots": wheel_slots,
                "active_wheel_index": active_wheel_index,
                "active_slot": active_slot,
                "calendar_slots": calendar_slots,
                "marquee_items": get_marquee_items(site_blocks),
                "gallery_teaser": gallery or GALLERY_TEASER,
                "gallery_from_db": bool(gallery),
                "hub_stats": get_hub_stats(site_blocks),
                "current_nav": "hub",
                "page_theme": active_slot.presentation.theme_class if active_slot else "theme-spring",
            }
        )
        return ctx


class ArchiveView(TemplateView):
    template_name = "tournaments/archive.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        editions = list(ArchiveEdition.objects.filter(is_published=True))
        gallery = get_archive_gallery()
        edition_rows = (
            [
                {
                    "year": edition.year,
                    "title": edition.title,
                    "season": edition.season,
                    "teams": edition.teams_count,
                    "matches": edition.matches_count,
                    "goals": edition.goals_count,
                    "theme_class": edition.theme_class,
                }
                for edition in editions
            ]
            if editions
            else ARCHIVE_EDITIONS
        )
        ctx.update(
            {
                "gallery": gallery or ARCHIVE_GALLERY,
                "gallery_from_db": bool(gallery),
                "editions": edition_rows,
                "current_nav": "archive",
                "page_theme": "theme-spring",
            }
        )
        return ctx


class TournamentDetailView(DetailView):
    model = Tournament
    template_name = "tournaments/detail.html"
    context_object_name = "tournament"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Tournament.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tournament = self.object
        teams_pool = get_teams_pool(tournament)
        schedule = get_schedule(tournament)
        bracket = get_bracket(tournament)
        top_scorers = get_top_scorers(tournament)
        ctx.update(
            {
                "current_nav": tournament.slug,
                "page_theme": tournament.theme_class,
                "bracket": bracket if bracket["r16"] or bracket["sf"] else BRACKET_MOCK,
                "schedule": schedule or SCHEDULE_MOCK,
                "top_scorers": top_scorers or TOP_SCORERS,
                "teams_pool": teams_pool or TEAMS_POOL[:16],
            }
        )
        return ctx


class ApplicationView(View):
    template_name = "tournaments/apply.html"

    def get(self, request, *args, **kwargs):
        preset = request.GET.get("tournament", "")
        tournaments = get_apply_tournaments()
        form = ApplicationForm(preset_slug=preset or None, open_tournaments=tournaments)
        tournament = None
        if preset:
            candidate = Tournament.objects.filter(slug=preset, is_published=True).first()
            if candidate and tournament_is_open_for_apply(candidate):
                tournament = candidate
        if not tournament and form.initial.get("tournament"):
            tournament = Tournament.objects.filter(pk=form.initial["tournament"]).first()
        if not tournament and tournaments:
            tournament = tournaments[0]
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "tournaments": tournaments,
                "selected_tournament": tournament,
                "current_nav": "apply",
                "page_theme": tournament.theme_class if tournament else "theme-spring",
            },
        )

    def post(self, request, *args, **kwargs):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            application.send_notification()
            if request.htmx:
                return render(
                    request,
                    "tournaments/partials/apply_success.html",
                    {"application": application},
                )
            return render(
                request,
                "tournaments/partials/apply_success.html",
                {"application": application},
            )
        if request.htmx:
            response = render(
                request,
                "tournaments/partials/apply_form.html",
                self._form_context(form, request.POST.get("tournament")),
            )
            response.status_code = 422
            return response
        return render(
            request,
            self.template_name,
            self._form_context(form, request.POST.get("tournament")),
            status=422,
        )

    def _form_context(self, form, tournament_id):
        tournaments = get_apply_tournaments()
        tournament = None
        if tournament_id:
            candidate = Tournament.objects.filter(pk=tournament_id).first()
            if candidate and tournament_is_open_for_apply(candidate):
                tournament = candidate
        if not tournament and tournaments:
            tournament = tournaments[0]
        return {
            "form": form,
            "tournaments": tournaments,
            "selected_tournament": tournament,
            "current_nav": "apply",
            "page_theme": tournament.theme_class if tournament else "theme-spring",
        }


class TournamentDataPartialView(View):
    """HTMX: return hero panel HTML for season wheel."""

    def get(self, request, slug):
        index = int(request.GET.get("index", 0))
        edition_year_raw = request.GET.get("edition_year")
        edition_year = int(edition_year_raw) if edition_year_raw else None

        wheel_slots, _ = get_home_season_timeline()
        slot = find_wheel_slot(slug, edition_year=edition_year)

        if slot is None:
            tournament = get_object_or_404(Tournament, slug=slug, is_published=True)
            return render(
                request,
                "tournaments/partials/hero_row.html",
                {
                    "tournament": presentation_from_db(tournament),
                    "is_virtual": False,
                    "apply_url": f"{reverse('tournaments:apply')}?tournament={tournament.slug}",
                    "detail_url": tournament.get_absolute_url(),
                    "index": index,
                    "tournaments_count": len(wheel_slots),
                },
            )

        return render(
            request,
            "tournaments/partials/hero_row.html",
            {
                "tournament": slot.presentation,
                "is_virtual": slot.is_virtual,
                "apply_url": slot.apply_url,
                "detail_url": slot.detail_url,
                "index": index,
                "tournaments_count": len(wheel_slots),
            },
        )
