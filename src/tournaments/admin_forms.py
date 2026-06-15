from django import forms
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE
from unfold.forms import AuthenticationForm

from src.tournaments.admin_guidelines import ACCENT_SPAN_BLOCK_KEYS, field_help
from src.tournaments.admin_validators import (
    validate_image_upload,
    validate_plain_text,
    validate_rich_text,
    validate_video_url,
)
from src.tournaments.models import GalleryImage, SiteBlock, SiteSettings, Tournament


class UkrainianAdminAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].label = _("Імʼя користувача")
        self.fields["password"].label = _("Пароль")

    error_messages = {
        "invalid_login": _(
            "Будь ласка, введіть правильні імʼя користувача та пароль. "
            "Зверніть увагу: обидва поля чутливі до регістру."
        ),
        "inactive": _("Цей обліковий запис неактивний."),
    }


class SiteBlockAdminForm(forms.ModelForm):
    class Meta:
        model = SiteBlock
        fields = "__all__"
        widgets = {
            "text_html": TinyMCE(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text_html"].help_text = field_help("text_html")
        self.fields["image"].help_text = field_help("siteblock_image")
        self.fields["video_url"].help_text = field_help("video_url")

    def clean_text_html(self):
        return self.cleaned_data.get("text_html", "")

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            validate_image_upload(image, "siteblock_image")
        return image

    def clean_video_url(self):
        return validate_video_url(self.cleaned_data.get("video_url", ""))

    def clean(self):
        cleaned = super().clean()
        content_type = cleaned.get("content_type")
        text_html = cleaned.get("text_html", "").strip()
        image = cleaned.get("image")
        video_url = cleaned.get("video_url", "").strip()
        has_image = image or (self.instance.pk and self.instance.image)

        if content_type == SiteBlock.ContentType.TEXT and not text_html:
            raise forms.ValidationError("Для текстового блоку заповніть поле «Текст (HTML)».")
        if content_type == SiteBlock.ContentType.IMAGE and not has_image:
            raise forms.ValidationError("Для фото-блоку завантажте зображення.")
        if content_type == SiteBlock.ContentType.VIDEO and not video_url:
            raise forms.ValidationError("Для відео-блоку вкажіть URL YouTube або Vimeo.")

        if content_type == SiteBlock.ContentType.TEXT and text_html:
            block_key = cleaned.get("key") or getattr(self.instance, "key", "")
            cleaned["text_html"] = validate_rich_text(
                text_html,
                field_key="text_html",
                allow_accent_span=block_key in ACCENT_SPAN_BLOCK_KEYS,
            )
        return cleaned


class SiteSettingsAdminForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["logo"].help_text = field_help("logo")
        self.fields["footer_about"].help_text = field_help("footer_about")
        self.fields["footer_copyright"].help_text = field_help("footer_copyright")
        self.fields["header_cta_label"].help_text = field_help("header_cta_label")

    def clean_logo(self):
        logo = self.cleaned_data.get("logo")
        if logo:
            validate_image_upload(logo, "logo")
        return logo

    def clean_footer_about(self):
        return validate_plain_text(self.cleaned_data.get("footer_about", ""), "footer_about")

    def clean_footer_copyright(self):
        return validate_plain_text(
            self.cleaned_data.get("footer_copyright", ""),
            "footer_copyright",
        )

    def clean_header_cta_label(self):
        return validate_plain_text(
            self.cleaned_data.get("header_cta_label", ""),
            "header_cta_label",
        )


class TournamentAdminForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = "__all__"
        widgets = {
            "description": TinyMCE(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].help_text = field_help("description")
        self.fields["hero_image"].help_text = field_help("hero_image")
        self.fields["card_image"].help_text = field_help("card_image")
        self.fields["tagline"].help_text = field_help("tagline")
        self.fields["highlight"].help_text = field_help("highlight")

    def clean_description(self):
        return validate_rich_text(
            self.cleaned_data.get("description", ""),
            field_key="description",
        )

    def clean_hero_image(self):
        image = self.cleaned_data.get("hero_image")
        if image:
            validate_image_upload(image, "tournament_hero")
        return image

    def clean_card_image(self):
        image = self.cleaned_data.get("card_image")
        if image:
            validate_image_upload(image, "tournament_card")
        return image

    def clean_tagline(self):
        return validate_plain_text(self.cleaned_data.get("tagline", ""), "tagline")

    def clean_highlight(self):
        return validate_plain_text(self.cleaned_data.get("highlight", ""), "highlight")


class GalleryImageAdminForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].help_text = field_help("gallery_image")
        self.fields["height"].help_text = field_help("gallery_height")

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            validate_image_upload(image, "gallery")
        return image
