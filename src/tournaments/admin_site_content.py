from __future__ import annotations

import re

from django import forms
from django.contrib import messages
from django.contrib.admin.sites import site as default_admin_site
from django.core.cache import cache
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .admin_guidelines import ACCENT_SPAN_BLOCK_KEYS, field_help, render_admin_warning_callout
from .admin_validators import validate_image_upload, validate_plain_text, validate_rich_text, validate_video_url
from .block_defaults import BLOCK_DEFAULTS
from .context_processors import SITE_BLOCKS_CACHE_KEY
from .models import SiteBlock, SiteSettings
from .site_content_registry import (
    ContentSection,
    LEGACY_SECTION_REDIRECTS,
    get_block_field_label,
    get_first_section_slug,
    get_section,
    iter_section_blocks,
    PLAIN_LABEL_KEYS,
)

SEASON_START_FIELD = "season_start"
SEASON_END_FIELD = "season_end"
CONTACT_PHONE_FIELD = "contact_phone"
CONTACT_EMAIL_FIELD = "contact_email"

STAT_VALUE_KEY = re.compile(r"^stat_\d+_value$")
STAT_TEXT_KEY = re.compile(r"^stat_\d+_(label|hint)$")
ASIDE_TEXT_KEY = re.compile(r"^aside_")
EYEBROW_KEY = re.compile(r".*_eyebrow$")
MULTILINE_PLAIN_KEYS = frozenset({"marquee", "hero_desc", "stats_aside", "success_desc", "cta_desc"})


def _is_inline_field(key: str) -> bool:
    return (
        bool(STAT_VALUE_KEY.match(key))
        or bool(STAT_TEXT_KEY.match(key))
        or bool(EYEBROW_KEY.match(key))
        or bool(ASIDE_TEXT_KEY.match(key))
        or key in PLAIN_LABEL_KEYS
        or key in {"stat_plus", "hero_eyebrow", "archive_btn_all", "copyright"}
        or (key.endswith("_title") and key not in ACCENT_SPAN_BLOCK_KEYS)
    )


def _is_multiline_plain(key: str) -> bool:
    return key in MULTILINE_PLAIN_KEYS


def _uses_accent_rich_text(key: str) -> bool:
    return key in ACCENT_SPAN_BLOCK_KEYS


def _inline_input_widget(*, wide: bool = False) -> forms.TextInput:
    css_class = "vTextField site-content-editor__inline-input"
    if wide:
        css_class += " site-content-editor__inline-input--wide"
    return forms.TextInput(attrs={"class": css_class})


def _textarea_widget(*, rows: int = 2, large: bool = False) -> forms.Textarea:
    css_class = "vLargeTextField site-content-editor__textarea site-content-editor__textarea--compact"
    if large:
        css_class = "vLargeTextField site-content-editor__textarea site-content-editor__textarea--large"
    return forms.Textarea(
        attrs={"rows": rows, "class": css_class},
    )


def _plain_field_key(key: str) -> str:
    if STAT_VALUE_KEY.match(key):
        return "stat_value"
    if _is_multiline_plain(key):
        return "block_paragraph"
    return "site_label"


def _display_plain_text(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", text).strip()


def _display_textarea_value(value: str) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    match = re.fullmatch(r"<p>(.*?)</p>", text, flags=re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text


def block_field_name(page: str, key: str, suffix: str) -> str:
    return f"block__{page}__{key}__{suffix}"


def load_section_blocks(section: ContentSection) -> dict[tuple[str, str], SiteBlock]:
    blocks: dict[tuple[str, str], SiteBlock] = {}
    for page, key in iter_section_blocks(section):
        block, _created = SiteBlock.objects.get_or_create(
            page=page,
            key=key,
            defaults={
                "label": get_block_field_label(page, key),
                "content_type": SiteBlock.ContentType.TEXT,
                "text_html": BLOCK_DEFAULTS.get((page, key), ""),
                "sort_order": 0,
                "is_active": True,
            },
        )
        blocks[(page, key)] = block
    return blocks


class SitePageContentForm(forms.Form):
    def __init__(
        self,
        page_slug: str,
        section: ContentSection,
        blocks: dict[tuple[str, str], SiteBlock],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.page_slug = page_slug
        self.section = section
        self.blocks = blocks

        if "contact_info" in section.extra_fields:
            site = SiteSettings.load()
            self.fields[CONTACT_PHONE_FIELD] = forms.CharField(
                label="Телефон",
                max_length=32,
                required=False,
                initial=site.phone,
                help_text="Показується в блоці контактів поруч із формою заявки.",
            )
            self.fields[CONTACT_EMAIL_FIELD] = forms.EmailField(
                label="Email",
                required=False,
                initial=site.email,
                help_text="Показується в блоці контактів поруч із формою заявки.",
            )

        if "season_dates" in section.extra_fields:
            site = SiteSettings.load()
            self.fields[SEASON_START_FIELD] = forms.DateField(
                label="Початок сезону",
                required=False,
                initial=site.season_start,
                widget=forms.DateInput(
                    attrs={"type": "date", "class": "site-content-editor__date-input"},
                ),
                help_text="Можна підставити в текст банера як {season_start}.",
            )
            self.fields[SEASON_END_FIELD] = forms.DateField(
                label="Кінець сезону",
                required=False,
                initial=site.season_end,
                widget=forms.DateInput(
                    attrs={"type": "date", "class": "site-content-editor__date-input"},
                ),
                help_text="Можна підставити в текст банера як {season_end}.",
            )

        for page, key in section.blocks:
            block = blocks[(page, key)]
            self._add_block_fields(block)

    def _add_block_fields(self, block: SiteBlock) -> None:
        page = block.page
        key = block.key
        field_label = get_block_field_label(page, key)

        if block.content_type == SiteBlock.ContentType.TEXT:
            if _is_inline_field(key):
                widget = _inline_input_widget()
                initial = _display_plain_text(block.text_html)
                help_key = _plain_field_key(key)
            elif _uses_accent_rich_text(key):
                widget = _inline_input_widget(wide=True)
                initial = _display_textarea_value(block.text_html)
                help_key = "text_html"
            elif _is_multiline_plain(key):
                widget = _textarea_widget(rows=6 if key == "marquee" else 3, large=key == "marquee")
                initial = _display_textarea_value(block.text_html)
                help_key = _plain_field_key(key)
            else:
                widget = _textarea_widget(rows=2)
                initial = _display_textarea_value(block.text_html)
                help_key = "text_html"

            text_field = block_field_name(page, key, "text_html")
            self.fields[text_field] = forms.CharField(
                label=field_label,
                initial=initial,
                required=False,
                widget=widget,
            )
            help_text = field_help(help_key)
            if _uses_accent_rich_text(key):
                help_text = 'Для жовтого акценту: <span class="text-accent">текст</span>.'
            elif help_key == "text_html":
                help_text = "Короткий текст без зображень. HTML — лише для полів з акцентом."
            if help_text:
                self.fields[text_field].help_text = help_text
            return

        if block.content_type == SiteBlock.ContentType.IMAGE:
            image_field = block_field_name(page, key, "image")
            self.fields[image_field] = forms.ImageField(
                label=field_label,
                required=False,
            )
            self.fields[image_field].help_text = field_help("siteblock_image")
            if block.image:
                self.fields[image_field].help_text += f" Поточне: {block.image.name}"
            return

        if block.content_type == SiteBlock.ContentType.VIDEO:
            video_field = block_field_name(page, key, "video_url")
            self.fields[video_field] = forms.URLField(
                label=field_label,
                initial=block.video_url,
                required=False,
            )
            self.fields[video_field].help_text = field_help("video_url")

    def clean(self):
        cleaned = super().clean()
        errors: list[str] = []

        if SEASON_START_FIELD in self.fields:
            start = cleaned.get(SEASON_START_FIELD)
            end = cleaned.get(SEASON_END_FIELD)
            if start and end and end < start:
                errors.append("Дата кінця сезону не може бути раніше за дату початку.")

        if CONTACT_PHONE_FIELD in self.fields:
            phone = cleaned.get(CONTACT_PHONE_FIELD, "").strip()
            email = cleaned.get(CONTACT_EMAIL_FIELD, "").strip()
            if not phone:
                errors.append("Вкажіть телефон для блоку контактів.")
            if not email:
                errors.append("Вкажіть email для блоку контактів.")

        for block in self.blocks.values():
            page = block.page
            key = block.key

            if block.content_type == SiteBlock.ContentType.TEXT:
                text_name = block_field_name(page, key, "text_html")
                text = cleaned.get(text_name, "").strip()
                if not text:
                    errors.append(f"«{get_block_field_label(page, key)}»: заповніть текст.")
                    continue
                try:
                    if _is_inline_field(key) or _is_multiline_plain(key):
                        cleaned[text_name] = validate_plain_text(text, _plain_field_key(key))
                    else:
                        cleaned[text_name] = validate_rich_text(
                            text,
                            field_key="text_html",
                            allow_accent_span=_uses_accent_rich_text(key),
                        )
                except DjangoValidationError as exc:
                    errors.extend(exc.messages)
            elif block.content_type == SiteBlock.ContentType.IMAGE:
                image = cleaned.get(block_field_name(page, key, "image"))
                has_image = image or block.image
                if not has_image:
                    errors.append(f"«{get_block_field_label(page, key)}»: завантажте зображення.")
                elif image:
                    try:
                        validate_image_upload(image, "siteblock_image")
                    except DjangoValidationError as exc:
                        errors.extend(exc.messages)
            elif block.content_type == SiteBlock.ContentType.VIDEO:
                url = cleaned.get(block_field_name(page, key, "video_url"), "").strip()
                if not url:
                    errors.append(f"«{get_block_field_label(page, key)}»: вкажіть URL відео.")
                else:
                    try:
                        cleaned[block_field_name(page, key, "video_url")] = validate_video_url(url)
                    except DjangoValidationError as exc:
                        errors.extend(exc.messages)

        if errors:
            raise forms.ValidationError(errors)
        return cleaned

    def save(self) -> None:
        if CONTACT_PHONE_FIELD in self.fields:
            site = SiteSettings.load()
            site.phone = self.cleaned_data.get(CONTACT_PHONE_FIELD, "")
            site.email = self.cleaned_data.get(CONTACT_EMAIL_FIELD, "")
            site.save(update_fields=["phone", "email"])

        if SEASON_START_FIELD in self.fields:
            site = SiteSettings.load()
            site.season_start = self.cleaned_data.get(SEASON_START_FIELD)
            site.season_end = self.cleaned_data.get(SEASON_END_FIELD)
            site.save(update_fields=["season_start", "season_end"])

        for block in self.blocks.values():
            page = block.page
            key = block.key
            block.is_active = True

            if block.content_type == SiteBlock.ContentType.TEXT:
                block.text_html = self.cleaned_data.get(
                    block_field_name(page, key, "text_html"),
                    "",
                )
            elif block.content_type == SiteBlock.ContentType.IMAGE:
                uploaded = self.cleaned_data.get(block_field_name(page, key, "image"))
                if uploaded:
                    block.image = uploaded
            elif block.content_type == SiteBlock.ContentType.VIDEO:
                block.video_url = self.cleaned_data.get(
                    block_field_name(page, key, "video_url"),
                    "",
                )

            block.save()

        site = SiteSettings.load()
        site_updates: list[str] = []
        cta_block = self.blocks.get(("header", "cta_label"))
        if cta_block and cta_block.content_type == SiteBlock.ContentType.TEXT:
            site.header_cta_label = cta_block.text_html.strip()
            site_updates.append("header_cta_label")
        about_block = self.blocks.get(("footer", "about"))
        if about_block and about_block.content_type == SiteBlock.ContentType.TEXT:
            site.footer_about = about_block.text_html.strip()
            site_updates.append("footer_about")
        copyright_block = self.blocks.get(("footer", "copyright"))
        if copyright_block and copyright_block.content_type == SiteBlock.ContentType.TEXT:
            site.footer_copyright = copyright_block.text_html.strip()
            site_updates.append("footer_copyright")
        if site_updates:
            site.save(update_fields=site_updates)

        cache.delete(SITE_BLOCKS_CACHE_KEY)


def _section_form_fields(form: SitePageContentForm, section: ContentSection) -> list[forms.BoundField]:
    keys = tuple(key for _page, key in section.blocks)
    return _bound_fields_for_keys(form, section, keys)


def _bound_fields_for_keys(
    form: SitePageContentForm,
    section: ContentSection,
    keys: tuple[str, ...],
) -> list[forms.BoundField]:
    fields: list[forms.BoundField] = []
    for key in keys:
        page = section.page_slug
        block = form.blocks.get((page, key))
        if block is None:
            continue
        names: list[str] = []
        if block.content_type == SiteBlock.ContentType.TEXT:
            names.append(block_field_name(page, key, "text_html"))
        elif block.content_type == SiteBlock.ContentType.IMAGE:
            names.append(block_field_name(page, key, "image"))
        elif block.content_type == SiteBlock.ContentType.VIDEO:
            names.append(block_field_name(page, key, "video_url"))
        for name in names:
            if name in form.fields:
                fields.append(form[name])
    return fields


def _extra_fieldsets(form: SitePageContentForm, section: ContentSection) -> list[tuple[str, list[forms.BoundField]]]:
    groups: list[tuple[str, list[forms.BoundField]]] = []
    if "season_dates" in section.extra_fields:
        season_fields = [
            form[name]
            for name in (SEASON_START_FIELD, SEASON_END_FIELD)
            if name in form.fields
        ]
        if season_fields:
            groups.append(("Дати сезону", season_fields))
    if "contact_info" in section.extra_fields:
        contact_fields = [
            form[name]
            for name in (CONTACT_PHONE_FIELD, CONTACT_EMAIL_FIELD)
            if name in form.fields
        ]
        if contact_fields:
            groups.append(("Контактні дані", contact_fields))
    return groups


def _section_fieldsets(
    form: SitePageContentForm,
    section: ContentSection,
) -> list[tuple[str, list[forms.BoundField]]]:
    fieldsets: list[tuple[str, list[forms.BoundField]]] = []

    if section.field_groups:
        for group in section.field_groups:
            fields = _bound_fields_for_keys(form, section, group.block_keys)
            if fields:
                fieldsets.append((group.title, fields))
    else:
        fields = _section_form_fields(form, section)
        if fields:
            fieldsets.append(("", fields))

    fieldsets = _extra_fieldsets(form, section) + fieldsets
    return fieldsets


def _section_admin_change_url(section: ContentSection) -> str:
    return reverse(
        f"admin:tournaments_{section.admin_model_name}_change",
        args=[SiteSettings.load().pk],
    )


def site_content_page_view(request, page_slug: str):
    try:
        section_slug = get_first_section_slug(page_slug)
        section = get_section(page_slug, section_slug)
    except KeyError as exc:
        raise Http404 from exc
    return HttpResponseRedirect(_section_admin_change_url(section))


def site_content_section_view(
    request,
    page_slug: str,
    section_slug: str,
    *,
    model_admin=None,
):
    legacy_key = (page_slug, section_slug)
    if legacy_key in LEGACY_SECTION_REDIRECTS:
        redirect_page, redirect_section = LEGACY_SECTION_REDIRECTS[legacy_key]
        section = get_section(redirect_page, redirect_section)
        return HttpResponseRedirect(_section_admin_change_url(section))

    try:
        section = get_section(page_slug, section_slug)
    except KeyError as exc:
        raise Http404 from exc

    blocks = load_section_blocks(section)

    if request.method == "POST":
        form = SitePageContentForm(page_slug, section, blocks, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"«{section.sidebar_title or section.title}» збережено.")
            return HttpResponseRedirect(_section_admin_change_url(section))
    else:
        form = SitePageContentForm(page_slug, section, blocks)

    opts = model_admin.model._meta if model_admin else SiteBlock._meta
    context = {
        **default_admin_site.each_context(request),
        "form": form,
        "section": section,
        "fieldsets": _section_fieldsets(form, section),
        "content_warning": render_admin_warning_callout("siteblock"),
        "preview_url": section.preview_url,
        "title": section.sidebar_title or section.title,
        "breadcrumb": (
            ("Контент сайту", None),
            (section.sidebar_title or section.title, None),
        ),
        "opts": opts,
        "has_view_permission": True,
        "add": False,
        "change": True,
        "is_popup": False,
        "save_as": False,
        "show_save": True,
        "show_save_and_continue": False,
        "show_save_and_add_another": False,
        "show_delete": False,
    }
    return render(request, "admin/tournaments/site_content_page.html", context)
