from django import forms

from .models import Application, Tournament

REQUIRED_FIELD_MSG = "Заповніть це поле."


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
            "team_name": forms.TextInput(attrs={"placeholder": "Напр. ФК «Левеня»"}),
            "age_category": forms.TextInput(attrs={"placeholder": "Напр. U-12"}),
            "coach_name": forms.TextInput(attrs={"placeholder": "ПІБ тренера"}),
            "city": forms.TextInput(attrs={"placeholder": "Місто команди"}),
            "phone": forms.TextInput(attrs={"placeholder": "+38 0XX XXX XX XX"}),
            "email": forms.EmailInput(attrs={"placeholder": "email@club.ua"}),
            "note": forms.Textarea(attrs={"rows": 4, "placeholder": "Додаткова інформація"}),
        }
        labels = {
            "team_name": "Назва команди",
            "age_category": "Вікова категорія",
            "coach_name": "Тренер / представник",
            "city": "Місто",
            "players_count": "Кількість гравців",
            "phone": "Номер телефону",
            "email": "E-mail",
            "note": "Додаткова інформація",
        }

    def __init__(self, *args, preset_slug: str | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages["required"] = REQUIRED_FIELD_MSG

        tournament = None
        if preset_slug:
            tournament = Tournament.objects.filter(slug=preset_slug, is_published=True).first()
        if not tournament and not self.is_bound:
            tournament = (
                Tournament.objects.filter(is_published=True).order_by("sort_order", "pk").first()
            )
        if tournament and not self.is_bound and not self.initial.get("tournament"):
            self.initial["tournament"] = tournament.pk
