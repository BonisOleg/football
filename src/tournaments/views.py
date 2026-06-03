from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import DetailView, TemplateView

from .forms import ApplicationForm
from .mock_data import (
    ARCHIVE_EDITIONS,
    ARCHIVE_GALLERY,
    BRACKET_MOCK,
    GALLERY_TEASER,
    MARQUEE_ITEMS,
    SCHEDULE_MOCK,
    TEAMS_POOL,
    TOP_SCORERS,
)
from .models import Application, ArchiveEdition, Tournament
from .services import (
    get_archive_gallery,
    get_bracket,
    get_gallery_teaser,
    get_schedule,
    get_teams_pool,
    get_top_scorers,
)


class HomeView(TemplateView):
    template_name = "tournaments/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tournaments = list(Tournament.objects.filter(is_published=True))
        gallery = get_gallery_teaser()
        ctx.update(
            {
                "tournaments": tournaments,
                "active_tournament": tournaments[0] if tournaments else None,
                "marquee_items": MARQUEE_ITEMS,
                "gallery_teaser": gallery or GALLERY_TEASER,
                "gallery_from_db": bool(gallery),
                "hub_stats": [
                    {"value": 208, "label": "Команд за рік", "hint": "ACROSS 4 EVENTS"},
                    {"value": 316, "label": "Матчів", "hint": "REGULAR + PLAYOFF"},
                    {"value": 1381, "label": "Голів", "hint": "2025 SEASON"},
                    {"value": 28, "label": "Міст-учасників", "hint": "UA + EU"},
                ],
                "current_nav": "hub",
                "page_theme": tournaments[0].theme_class if tournaments else "theme-spring",
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
        form = ApplicationForm(preset_slug=preset or None)
        tournament = None
        if preset:
            tournament = Tournament.objects.filter(slug=preset, is_published=True).first()
        if not tournament and form.initial.get("tournament"):
            tournament = Tournament.objects.filter(pk=form.initial["tournament"]).first()
        if not tournament:
            tournament = Tournament.objects.filter(is_published=True).first()
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "tournaments": Tournament.objects.filter(is_published=True),
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
        tournament = None
        if tournament_id:
            tournament = Tournament.objects.filter(pk=tournament_id).first()
        if not tournament:
            tournament = Tournament.objects.filter(is_published=True).first()
        return {
            "form": form,
            "tournaments": Tournament.objects.filter(is_published=True),
            "selected_tournament": tournament,
            "current_nav": "apply",
            "page_theme": tournament.theme_class if tournament else "theme-spring",
        }


class TournamentDataPartialView(View):
    """HTMX: return hero panel HTML for season wheel."""

    def get(self, request, slug):
        tournament = get_object_or_404(Tournament, slug=slug, is_published=True)
        index = int(request.GET.get("index", 0))
        count = Tournament.objects.filter(is_published=True).count()
        return render(
            request,
            "tournaments/partials/hero_row.html",
            {
                "tournament": tournament,
                "index": index,
                "tournaments_count": count,
            },
        )
