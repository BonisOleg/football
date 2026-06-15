from django import forms

from .models import Application, Tournament
from .services import get_apply_tournaments, tournament_is_open_for_apply
from .utils.site_block_text import get_plain_block_text

APPLY_FIELD_BLOCKS: dict[str, tuple[str, str]] = {
    "team_name": ("field_team_name_label", "field_team_name_ph"),
    "age_category": ("field_age_category_label", "field_age_category_ph"),
    "coach_name": ("field_coach_name_label", "field_coach_name_ph"),
    "city": ("field_city_label", "field_city_ph"),
    "players_count": ("field_players_count_label", ""),
    "phone": ("field_phone_label", "field_phone_ph"),
    "email": ("field_email_label", "field_email_ph"),
    "note": ("field_note_label", "field_note_ph"),
}


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "tournament",
            "team_name",
            "age_category",
            "coach_name",
            "city",
            "players_count",
            "phone",
            "email",
            "note",
        ]
        widgets = {
            "tournament": forms.HiddenInput(),
            "team_name": forms.TextInput(),
            "age_category": forms.TextInput(),
            "coach_name": forms.TextInput(),
            "city": forms.TextInput(),
            "phone": forms.TextInput(),
            "email": forms.EmailInput(),
            "note": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(
        self,
        *args,
        preset_slug: str | None = None,
        open_tournaments: list[Tournament] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        required_msg = get_plain_block_text("apply", "required_error_msg", fallback="Заповніть це поле.")
        for field in self.fields.values():
            field.error_messages["required"] = required_msg

        for name, (label_key, placeholder_key) in APPLY_FIELD_BLOCKS.items():
            field = self.fields[name]
            field.label = get_plain_block_text("apply", label_key)
            if placeholder_key:
                field.widget.attrs["placeholder"] = get_plain_block_text("apply", placeholder_key)

        open_tournaments = open_tournaments if open_tournaments is not None else get_apply_tournaments()
        open_ids = [tournament.pk for tournament in open_tournaments]
        self.fields["tournament"].queryset = Tournament.objects.filter(pk__in=open_ids)

        tournament = None
        if preset_slug:
            candidate = Tournament.objects.filter(slug=preset_slug, is_published=True).first()
            if candidate and tournament_is_open_for_apply(candidate):
                tournament = candidate
        if not tournament and not self.is_bound and open_tournaments:
            tournament = open_tournaments[0]
        if tournament and not self.is_bound and not self.initial.get("tournament"):
            self.initial["tournament"] = tournament.pk
