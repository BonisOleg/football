from django.urls import path

from . import views

app_name = "tournaments"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("arxiv/", views.ArchiveView.as_view(), name="archive"),
    path("zayavka/", views.ApplicationView.as_view(), name="apply"),
    path(
        "partials/hero/<slug:slug>/",
        views.TournamentDataPartialView.as_view(),
        name="hero_partial",
    ),
    path("<slug:slug>/", views.TournamentDetailView.as_view(), name="detail"),
]
