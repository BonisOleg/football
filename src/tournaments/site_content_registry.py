from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, Literal

from django.urls import reverse_lazy


@dataclass(frozen=True)
class FieldGroup:
    title: str
    block_keys: tuple[str, ...]


@dataclass(frozen=True)
class ContentSection:
    slug: str
    page_slug: str
    title: str
    blocks: tuple[tuple[str, str], ...]
    sidebar_title: str = ""
    sidebar_icon: str = "edit_note"
    preview_url: str = "/"
    description: str = ""
    extra_fields: tuple[str, ...] = field(default_factory=tuple)
    field_groups: tuple[FieldGroup, ...] = field(default_factory=tuple)
    admin_model_name: str = ""
    sidebar_group: Literal["content", "archive"] = "content"


BLOCK_FIELD_LABELS: dict[tuple[str, str], str] = {
    ("home", "hero_eyebrow"): "Текст у зеленій мітці",
    ("home", "marquee"): "Пункти бігучого рядка (кожен з нового рядка)",
    ("home", "stats_eyebrow"): "Малий заголовок секції",
    ("home", "stats_title"): "Заголовок секції",
    ("home", "stats_aside"): "Текст праворуч від заголовка",
    ("home", "calendar_eyebrow"): "Малий заголовок секції",
    ("home", "calendar_title"): "Заголовок секції",
    ("home", "archive_eyebrow"): "Малий заголовок секції",
    ("home", "archive_title"): "Заголовок секції",
    ("home", "archive_btn_all"): "Текст кнопки «Дивитись усе»",
    ("home", "location_tag"): "Мітка локації над hero",
    ("home", "label_dates"): "Підпис «Дати»",
    ("home", "label_teams"): "Підпис «Команд»",
    ("home", "label_location"): "Підпис «Локація»",
    ("home", "label_format"): "Підпис «Формат»",
    ("home", "soon_badge"): "Мітка «Скоро»",
    ("home", "hero_btn_detail"): "Кнопка «Перейти до турніру»",
    ("home", "hero_btn_apply"): "Кнопка «Подати заявку»",
    ("home", "hero_btn_soon"): "Кнопка «Скоро» (неактивна)",
    ("home", "hero_swipe_touch"): "Підказка для мобільних",
    ("home", "hero_swipe_drag"): "Підказка для десктопу",
    ("home", "countdown_days"): "Таймер — дні",
    ("home", "countdown_hours"): "Таймер — години",
    ("home", "countdown_mins"): "Таймер — хвилини",
    ("home", "countdown_secs"): "Таймер — секунди",
    ("home", "stat_plus"): "Знак «+» після цифри",
    ("apply", "hero_eyebrow"): "Рядок над заголовком",
    ("apply", "hero_title"): "Заголовок",
    ("apply", "hero_desc"): "Короткий опис",
    ("apply", "aside_eyebrow"): "Мітка над заголовком",
    ("apply", "aside_title"): "Заголовок блоку контактів",
    ("apply", "aside_desc"): "Короткий опис",
    ("apply", "aside_phone_label"): "Підпис «Телефон»",
    ("apply", "aside_email_label"): "Підпис «Email»",
    ("apply", "aside_tournament_label"): "Підпис «Обраний турнір»",
    ("archive", "hero_eyebrow"): "Рядок над заголовком",
    ("archive", "hero_title"): "Заголовок",
    ("archive", "hero_desc"): "Короткий опис",
    ("archive", "editions_eyebrow"): "Малий заголовок секції",
    ("archive", "editions_title"): "Заголовок секції",
    ("archive", "label_teams"): "Підпис «Команд»",
    ("archive", "label_matches"): "Підпис «Матчів»",
    ("archive", "label_goals"): "Підпис «Голів»",
    ("archive", "gallery_eyebrow"): "Малий заголовок галереї",
    ("archive", "gallery_title"): "Заголовок галереї",
    ("footer", "copyright"): "Рядок copyright",
    ("footer", "about"): "Текст про організацію",
    ("footer", "col_tournaments"): "Заголовок колонки «Турніри»",
    ("footer", "col_contacts"): "Заголовок колонки «Контакти»",
    ("footer", "col_social"): "Заголовок колонки «Соцмережі»",
    ("footer", "tagline"): "Нижній рядок футера",
    ("footer", "dev_credit_text"): "Текст «Сайт розроблено»",
    ("header", "cta_label"): "Текст кнопки CTA",
    ("header", "nav_home"): "Пункт меню «Головна»",
    ("header", "nav_apply"): "Пункт меню «Заявка»",
    ("header", "nav_archive"): "Пункт меню «Архів»",
    ("header", "menu_sr_label"): "Підпис бургер-меню (sr-only)",
    ("header", "nav_aria_label"): "Aria-label навігації",
    ("header", "wordmark_primary"): "Wordmark — перша частина",
    ("header", "wordmark_accent"): "Wordmark — акцентна частина",
    ("apply", "form_tournament_eyebrow"): "Eyebrow кроку «Турнір»",
    ("apply", "form_tournament_title"): "Заголовок кроку «Турнір»",
    ("apply", "form_team_eyebrow"): "Eyebrow кроку «Команда»",
    ("apply", "form_team_title"): "Заголовок кроку «Команда»",
    ("apply", "submit_btn"): "Текст кнопки submit",
    ("apply", "form_error_title"): "Заголовок помилки форми",
    ("apply", "form_error_desc"): "Опис помилки форми",
    ("apply", "required_error_msg"): "Повідомлення для обовʼязкового поля",
    ("apply", "field_team_name_label"): "Поле — назва команди (label)",
    ("apply", "field_team_name_ph"): "Поле — назва команди (placeholder)",
    ("apply", "field_age_category_label"): "Поле — вікова категорія (label)",
    ("apply", "field_age_category_ph"): "Поле — вікова категорія (placeholder)",
    ("apply", "field_coach_name_label"): "Поле — тренер (label)",
    ("apply", "field_coach_name_ph"): "Поле — тренер (placeholder)",
    ("apply", "field_city_label"): "Поле — місто (label)",
    ("apply", "field_city_ph"): "Поле — місто (placeholder)",
    ("apply", "field_players_count_label"): "Поле — кількість гравців (label)",
    ("apply", "field_phone_label"): "Поле — телефон (label)",
    ("apply", "field_phone_ph"): "Поле — телефон (placeholder)",
    ("apply", "field_email_label"): "Поле — email (label)",
    ("apply", "field_email_ph"): "Поле — email (placeholder)",
    ("apply", "field_note_label"): "Поле — примітка (label)",
    ("apply", "field_note_ph"): "Поле — примітка (placeholder)",
    ("apply", "success_eyebrow"): "Eyebrow success-екрану",
    ("apply", "success_title_prefix"): "Префікс заголовка success",
    ("apply", "success_desc"): "Текст success-екрану",
    ("apply", "success_btn_tournament"): "Кнопка «До сторінки турніру»",
    ("apply", "success_btn_home"): "Кнопка «На головну»",
    ("detail", "btn_all_tournaments"): "Кнопка «Всі турніри»",
    ("detail", "about_eyebrow"): "Eyebrow «Про турнір»",
    ("detail", "about_label_fee"): "Підпис «Внесок»",
    ("detail", "about_label_prizes"): "Підпис «Нагороди»",
    ("detail", "currency_suffix"): "Символ валюти",
    ("detail", "bracket_eyebrow"): "Eyebrow «Сітка»",
    ("detail", "bracket_title"): "Заголовок «Сітка»",
    ("detail", "bracket_qf"): "Підпис «1/4 фіналу»",
    ("detail", "bracket_sf"): "Підпис «1/2 фіналу»",
    ("detail", "bracket_final"): "Підпис «Фінал»",
    ("detail", "schedule_eyebrow"): "Eyebrow «Розклад»",
    ("detail", "schedule_title"): "Заголовок «Розклад»",
    ("detail", "col_day"): "Колонка «День»",
    ("detail", "col_time"): "Колонка «Час»",
    ("detail", "col_match"): "Колонка «Матч»",
    ("detail", "col_age"): "Колонка «Вік»",
    ("detail", "col_score"): "Колонка «Рах.»",
    ("detail", "col_field"): "Колонка «Поле»",
    ("detail", "stats_eyebrow"): "Eyebrow «Статистика»",
    ("detail", "stats_title"): "Заголовок «Статистика»",
    ("detail", "label_wins"): "Підпис «Перемог»",
    ("detail", "label_losses"): "Підпис «Поразок»",
    ("detail", "teams_eyebrow"): "Eyebrow «Команди»",
    ("detail", "teams_title"): "Заголовок «Команди»",
    ("detail", "cta_eyebrow"): "Eyebrow CTA",
    ("detail", "cta_title"): "Заголовок CTA",
    ("detail", "cta_desc"): "Опис CTA",
    ("site", "default_title"): "Title за замовчуванням",
    ("site", "default_meta_description"): "Meta description за замовчуванням",
    ("site", "brand_suffix"): "Суфікс бренду в title",
    ("site", "home_page_title"): "Title головної",
    ("site", "apply_page_title"): "Title заявки",
    ("site", "archive_page_title"): "Title архіву",
    ("site", "wheel_prev_aria"): "Aria-label «Попередній сезон»",
    ("site", "wheel_next_aria"): "Aria-label «Наступний сезон»",
}


def _stat_block_labels(index: int) -> None:
    BLOCK_FIELD_LABELS[("home", f"stat_{index}_value")] = "Число"
    BLOCK_FIELD_LABELS[("home", f"stat_{index}_label")] = "Підпис під числом"
    BLOCK_FIELD_LABELS[("home", f"stat_{index}_hint")] = "Додатковий рядок (латиницею)"


for _idx in range(1, 5):
    _stat_block_labels(_idx)

PLAIN_LABEL_KEYS: frozenset[str] = frozenset(
    {
        "archive_btn_all",
        "location_tag",
        "label_dates",
        "label_teams",
        "label_location",
        "label_format",
        "soon_badge",
        "hero_btn_detail",
        "hero_btn_apply",
        "hero_btn_soon",
        "hero_swipe_touch",
        "hero_swipe_drag",
        "countdown_days",
        "countdown_hours",
        "countdown_mins",
        "countdown_secs",
        "stat_plus",
        "label_matches",
        "label_goals",
        "cta_label",
        "nav_home",
        "nav_apply",
        "nav_archive",
        "menu_sr_label",
        "nav_aria_label",
        "wordmark_primary",
        "wordmark_accent",
        "col_tournaments",
        "col_contacts",
        "col_social",
        "tagline",
        "dev_credit_text",
        "form_tournament_eyebrow",
        "form_tournament_title",
        "form_team_eyebrow",
        "form_team_title",
        "submit_btn",
        "form_error_title",
        "form_error_desc",
        "required_error_msg",
        "field_team_name_label",
        "field_team_name_ph",
        "field_age_category_label",
        "field_age_category_ph",
        "field_coach_name_label",
        "field_coach_name_ph",
        "field_city_label",
        "field_city_ph",
        "field_players_count_label",
        "field_phone_label",
        "field_phone_ph",
        "field_email_label",
        "field_email_ph",
        "field_note_label",
        "field_note_ph",
        "success_eyebrow",
        "success_title_prefix",
        "success_btn_tournament",
        "success_btn_home",
        "btn_all_tournaments",
        "about_eyebrow",
        "about_label_fee",
        "about_label_prizes",
        "currency_suffix",
        "bracket_eyebrow",
        "bracket_title",
        "bracket_qf",
        "bracket_sf",
        "bracket_final",
        "schedule_eyebrow",
        "schedule_title",
        "col_day",
        "col_time",
        "col_match",
        "col_age",
        "col_score",
        "col_field",
        "stats_eyebrow",
        "stats_title",
        "label_wins",
        "label_losses",
        "teams_eyebrow",
        "teams_title",
        "cta_eyebrow",
        "default_title",
        "default_meta_description",
        "brand_suffix",
        "home_page_title",
        "apply_page_title",
        "archive_page_title",
        "wheel_prev_aria",
        "wheel_next_aria",
    }
)

STAT_BLOCK_KEYS: tuple[str, ...] = tuple(
    key
    for index in range(1, 5)
    for key in (f"stat_{index}_value", f"stat_{index}_label", f"stat_{index}_hint")
)


def get_block_field_label(page: str, key: str) -> str:
    return BLOCK_FIELD_LABELS.get((page, key), key.replace("_", " ").capitalize())


def _home_stat_blocks() -> tuple[tuple[str, str], ...]:
    blocks: list[tuple[str, str]] = [
        ("home", "stats_eyebrow"),
        ("home", "stats_title"),
        ("home", "stats_aside"),
        ("home", "stat_plus"),
    ]
    for key in STAT_BLOCK_KEYS:
        blocks.append(("home", key))
    return tuple(blocks)


def _home_stat_field_groups() -> tuple[FieldGroup, ...]:
    groups: list[FieldGroup] = [
        FieldGroup(
            "Заголовок секції",
            ("stats_eyebrow", "stats_title", "stats_aside", "stat_plus"),
        ),
    ]
    for index in range(1, 5):
        prefix = f"stat_{index}"
        groups.append(
            FieldGroup(
                f"Показник {index}",
                (f"{prefix}_value", f"{prefix}_label", f"{prefix}_hint"),
            )
        )
    return tuple(groups)


CONTENT_SECTIONS: tuple[ContentSection, ...] = (
    ContentSection(
        slug="hero",
        page_slug="home",
        title="Головний банер",
        sidebar_title="Головний банер",
        sidebar_icon="image",
        preview_url="/",
        admin_model_name="homeherosettings",
        description=(
            "Текст у зеленій мітці, мітка локації, дати сезону та кнопки hero. "
            "Можна використати {year}, {season_start}, {season_end}."
        ),
        blocks=(
            ("home", "hero_eyebrow"),
            ("home", "location_tag"),
            ("home", "hero_btn_detail"),
            ("home", "hero_btn_apply"),
            ("home", "hero_btn_soon"),
            ("home", "hero_swipe_touch"),
            ("home", "hero_swipe_drag"),
        ),
        extra_fields=("season_dates",),
        field_groups=(
            FieldGroup("Мітка та локація", ("hero_eyebrow", "location_tag")),
            FieldGroup(
                "Кнопки",
                ("hero_btn_detail", "hero_btn_apply", "hero_btn_soon"),
            ),
            FieldGroup("Підказки", ("hero_swipe_touch", "hero_swipe_drag")),
        ),
    ),
    ContentSection(
        slug="marquee",
        page_slug="home",
        title="Бігучий рядок",
        sidebar_title="Бігучий рядок",
        sidebar_icon="view_carousel",
        preview_url="/",
        admin_model_name="homemarqueesettings",
        description="Один рядок — один пункт бігучого рядка.",
        blocks=(("home", "marquee"),),
        field_groups=(FieldGroup("Пункти рядка", ("marquee",)),),
    ),
    ContentSection(
        slug="season-stats",
        page_slug="home",
        title="Один рік 4 турніри",
        sidebar_title="Секція «Один рік 4 турніри»",
        sidebar_icon="pin",
        preview_url="/",
        admin_model_name="homeseasonstatssettings",
        blocks=_home_stat_blocks(),
        field_groups=_home_stat_field_groups(),
    ),
    ContentSection(
        slug="calendar",
        page_slug="home",
        title="Календар сезону",
        sidebar_title="Секція «Календар сезону»",
        sidebar_icon="calendar_month",
        preview_url="/",
        admin_model_name="homecalendarsettings",
        description="Заголовки секції, підписи карток і таймер зворотного відліку.",
        blocks=(
            ("home", "calendar_eyebrow"),
            ("home", "calendar_title"),
            ("home", "label_dates"),
            ("home", "label_teams"),
            ("home", "label_location"),
            ("home", "label_format"),
            ("home", "soon_badge"),
            ("home", "countdown_days"),
            ("home", "countdown_hours"),
            ("home", "countdown_mins"),
            ("home", "countdown_secs"),
        ),
        field_groups=(
            FieldGroup("Заголовок секції", ("calendar_eyebrow", "calendar_title")),
            FieldGroup(
                "Підписи карток",
                ("label_dates", "label_teams", "label_location", "label_format", "soon_badge"),
            ),
            FieldGroup(
                "Таймер",
                ("countdown_days", "countdown_hours", "countdown_mins", "countdown_secs"),
            ),
        ),
    ),
    ContentSection(
        slug="archive-teaser",
        page_slug="home",
        title="Архів на головній",
        sidebar_title="Секція «Архів на головній»",
        sidebar_icon="inventory_2",
        preview_url="/",
        admin_model_name="homearchiveteasersettings",
        blocks=(
            ("home", "archive_eyebrow"),
            ("home", "archive_title"),
            ("home", "archive_btn_all"),
        ),
        field_groups=(
            FieldGroup(
                "Заголовок і кнопка",
                ("archive_eyebrow", "archive_title", "archive_btn_all"),
            ),
        ),
    ),
    ContentSection(
        slug="hero",
        page_slug="apply",
        title="Банер заявки",
        sidebar_title="Секція «Банер заявки»",
        sidebar_icon="assignment",
        preview_url="/zayavka/",
        admin_model_name="applyherosettings",
        blocks=(
            ("apply", "hero_eyebrow"),
            ("apply", "hero_title"),
            ("apply", "hero_desc"),
        ),
        field_groups=(
            FieldGroup("Банер", ("hero_eyebrow", "hero_title", "hero_desc")),
        ),
    ),
    ContentSection(
        slug="aside",
        page_slug="apply",
        title="Контакти заявки",
        sidebar_title="Секція «Контакти заявки»",
        sidebar_icon="contact_mail",
        preview_url="/zayavka/",
        admin_model_name="applyasidesettings",
        description=(
            "Блок праворуч від форми заявки. "
            "Назву та дати обраного турніру підставляє сайт автоматично."
        ),
        blocks=(
            ("apply", "aside_eyebrow"),
            ("apply", "aside_title"),
            ("apply", "aside_desc"),
            ("apply", "aside_phone_label"),
            ("apply", "aside_email_label"),
            ("apply", "aside_tournament_label"),
        ),
        extra_fields=("contact_info",),
        field_groups=(
            FieldGroup(
                "Тексти блоку",
                ("aside_eyebrow", "aside_title", "aside_desc"),
            ),
            FieldGroup(
                "Підписи полів",
                ("aside_phone_label", "aside_email_label", "aside_tournament_label"),
            ),
        ),
    ),
    ContentSection(
        slug="hero",
        page_slug="archive",
        title="Банер архіву",
        sidebar_title="Банер архіву",
        sidebar_icon="inventory_2",
        preview_url="/arxiv/",
        admin_model_name="archiveherosettings",
        sidebar_group="archive",
        blocks=(
            ("archive", "hero_eyebrow"),
            ("archive", "hero_title"),
            ("archive", "hero_desc"),
        ),
        field_groups=(
            FieldGroup("Банер", ("hero_eyebrow", "hero_title", "hero_desc")),
        ),
    ),
    ContentSection(
        slug="editions",
        page_slug="archive",
        title="Результати за роки",
        sidebar_title="Секція «Результати за роки»",
        sidebar_icon="leaderboard",
        preview_url="/arxiv/",
        admin_model_name="archiveeditionssectionsettings",
        sidebar_group="archive",
        description="Заголовок секції та підписи статистики на картках архіву.",
        blocks=(
            ("archive", "editions_eyebrow"),
            ("archive", "editions_title"),
            ("archive", "label_teams"),
            ("archive", "label_matches"),
            ("archive", "label_goals"),
        ),
        field_groups=(
            FieldGroup("Заголовок секції", ("editions_eyebrow", "editions_title")),
            FieldGroup(
                "Підписи статистики",
                ("label_teams", "label_matches", "label_goals"),
            ),
        ),
    ),
    ContentSection(
        slug="gallery",
        page_slug="archive",
        title="Галерея архіву",
        sidebar_title="Секція «Галерея архіву»",
        sidebar_icon="photo_library",
        preview_url="/arxiv/",
        admin_model_name="archivegallerysectionsettings",
        sidebar_group="archive",
        blocks=(
            ("archive", "gallery_eyebrow"),
            ("archive", "gallery_title"),
        ),
        field_groups=(
            FieldGroup("Заголовок галереї", ("gallery_eyebrow", "gallery_title")),
        ),
    ),
    ContentSection(
        slug="copyright",
        page_slug="footer",
        title="Футер",
        sidebar_title="Футер",
        sidebar_icon="bottom_navigation",
        preview_url="/",
        admin_model_name="footersettings",
        description="Тексти футера. У copyright використовуйте {year} для поточного року.",
        blocks=(
            ("footer", "about"),
            ("footer", "copyright"),
            ("footer", "col_tournaments"),
            ("footer", "col_contacts"),
            ("footer", "col_social"),
            ("footer", "tagline"),
            ("footer", "dev_credit_text"),
        ),
        field_groups=(
            FieldGroup("Про організацію", ("about",)),
            FieldGroup("Copyright", ("copyright",)),
            FieldGroup(
                "Колонки",
                ("col_tournaments", "col_contacts", "col_social"),
            ),
            FieldGroup("Низ футера", ("tagline", "dev_credit_text")),
        ),
    ),
    ContentSection(
        slug="navigation",
        page_slug="header",
        title="Хедер і навігація",
        sidebar_title="Хедер і навігація",
        sidebar_icon="menu",
        preview_url="/",
        admin_model_name="headernavigationsettings",
        description="Меню, wordmark і кнопка CTA в хедері.",
        blocks=(
            ("header", "cta_label"),
            ("header", "nav_home"),
            ("header", "nav_apply"),
            ("header", "nav_archive"),
            ("header", "menu_sr_label"),
            ("header", "nav_aria_label"),
            ("header", "wordmark_primary"),
            ("header", "wordmark_accent"),
        ),
        field_groups=(
            FieldGroup("Кнопка CTA", ("cta_label",)),
            FieldGroup(
                "Меню",
                ("nav_home", "nav_apply", "nav_archive", "menu_sr_label", "nav_aria_label"),
            ),
            FieldGroup("Wordmark", ("wordmark_primary", "wordmark_accent")),
        ),
    ),
    ContentSection(
        slug="form",
        page_slug="apply",
        title="Форма заявки",
        sidebar_title="Форма заявки",
        sidebar_icon="edit_document",
        preview_url="/zayavka/",
        admin_model_name="applyformsettings",
        description="Підписи, placeholder-и та кроки форми заявки.",
        blocks=(
            ("apply", "form_tournament_eyebrow"),
            ("apply", "form_tournament_title"),
            ("apply", "form_team_eyebrow"),
            ("apply", "form_team_title"),
            ("apply", "submit_btn"),
            ("apply", "form_error_title"),
            ("apply", "form_error_desc"),
            ("apply", "required_error_msg"),
            ("apply", "field_team_name_label"),
            ("apply", "field_team_name_ph"),
            ("apply", "field_age_category_label"),
            ("apply", "field_age_category_ph"),
            ("apply", "field_coach_name_label"),
            ("apply", "field_coach_name_ph"),
            ("apply", "field_city_label"),
            ("apply", "field_city_ph"),
            ("apply", "field_players_count_label"),
            ("apply", "field_phone_label"),
            ("apply", "field_phone_ph"),
            ("apply", "field_email_label"),
            ("apply", "field_email_ph"),
            ("apply", "field_note_label"),
            ("apply", "field_note_ph"),
        ),
        field_groups=(
            FieldGroup(
                "Кроки форми",
                (
                    "form_tournament_eyebrow",
                    "form_tournament_title",
                    "form_team_eyebrow",
                    "form_team_title",
                    "submit_btn",
                ),
            ),
            FieldGroup(
                "Помилки",
                ("form_error_title", "form_error_desc", "required_error_msg"),
            ),
            FieldGroup(
                "Назва команди",
                ("field_team_name_label", "field_team_name_ph"),
            ),
            FieldGroup(
                "Вікова категорія",
                ("field_age_category_label", "field_age_category_ph"),
            ),
            FieldGroup(
                "Тренер",
                ("field_coach_name_label", "field_coach_name_ph"),
            ),
            FieldGroup(
                "Місто",
                ("field_city_label", "field_city_ph"),
            ),
            FieldGroup("Кількість гравців", ("field_players_count_label",)),
            FieldGroup(
                "Телефон",
                ("field_phone_label", "field_phone_ph"),
            ),
            FieldGroup(
                "Email",
                ("field_email_label", "field_email_ph"),
            ),
            FieldGroup(
                "Примітка",
                ("field_note_label", "field_note_ph"),
            ),
        ),
    ),
    ContentSection(
        slug="success",
        page_slug="apply",
        title="Після заявки",
        sidebar_title="Після заявки",
        sidebar_icon="task_alt",
        preview_url="/zayavka/",
        admin_model_name="applysuccesssettings",
        description="Екран після успішного відправлення заявки.",
        blocks=(
            ("apply", "success_eyebrow"),
            ("apply", "success_title_prefix"),
            ("apply", "success_desc"),
            ("apply", "success_btn_tournament"),
            ("apply", "success_btn_home"),
        ),
        field_groups=(
            FieldGroup(
                "Тексти",
                ("success_eyebrow", "success_title_prefix", "success_desc"),
            ),
            FieldGroup(
                "Кнопки",
                ("success_btn_tournament", "success_btn_home"),
            ),
        ),
    ),
    ContentSection(
        slug="page",
        page_slug="detail",
        title="Сторінка турніру",
        sidebar_title="Сторінка турніру",
        sidebar_icon="sports_soccer",
        preview_url="/",
        admin_model_name="detailpagesettings",
        description="UI-підписи сторінки турніру. Дані турніру редагуються в «Сезони».",
        blocks=(
            ("detail", "btn_all_tournaments"),
            ("detail", "about_eyebrow"),
            ("detail", "about_label_fee"),
            ("detail", "about_label_prizes"),
            ("detail", "currency_suffix"),
            ("detail", "bracket_eyebrow"),
            ("detail", "bracket_title"),
            ("detail", "bracket_qf"),
            ("detail", "bracket_sf"),
            ("detail", "bracket_final"),
            ("detail", "schedule_eyebrow"),
            ("detail", "schedule_title"),
            ("detail", "col_day"),
            ("detail", "col_time"),
            ("detail", "col_match"),
            ("detail", "col_age"),
            ("detail", "col_score"),
            ("detail", "col_field"),
            ("detail", "stats_eyebrow"),
            ("detail", "stats_title"),
            ("detail", "label_wins"),
            ("detail", "label_losses"),
            ("detail", "teams_eyebrow"),
            ("detail", "teams_title"),
            ("detail", "cta_eyebrow"),
            ("detail", "cta_title"),
            ("detail", "cta_desc"),
        ),
        field_groups=(
            FieldGroup("Hero", ("btn_all_tournaments",)),
            FieldGroup(
                "Про турнір",
                ("about_eyebrow", "about_label_fee", "about_label_prizes", "currency_suffix"),
            ),
            FieldGroup(
                "Сітка",
                ("bracket_eyebrow", "bracket_title", "bracket_qf", "bracket_sf", "bracket_final"),
            ),
            FieldGroup(
                "Розклад",
                (
                    "schedule_eyebrow",
                    "schedule_title",
                    "col_day",
                    "col_time",
                    "col_match",
                    "col_age",
                    "col_score",
                    "col_field",
                ),
            ),
            FieldGroup(
                "Статистика",
                ("stats_eyebrow", "stats_title", "label_wins", "label_losses"),
            ),
            FieldGroup("Команди", ("teams_eyebrow", "teams_title")),
            FieldGroup("CTA", ("cta_eyebrow", "cta_title", "cta_desc")),
        ),
    ),
    ContentSection(
        slug="seo",
        page_slug="site",
        title="SEO і заголовки",
        sidebar_title="SEO і заголовки",
        sidebar_icon="travel_explore",
        preview_url="/",
        admin_model_name="siteseosettings",
        description="Title сторінок, meta description і aria-labels hero-колеса.",
        blocks=(
            ("site", "default_title"),
            ("site", "default_meta_description"),
            ("site", "brand_suffix"),
            ("site", "home_page_title"),
            ("site", "apply_page_title"),
            ("site", "archive_page_title"),
            ("site", "wheel_prev_aria"),
            ("site", "wheel_next_aria"),
        ),
        field_groups=(
            FieldGroup(
                "Загальні",
                ("default_title", "default_meta_description", "brand_suffix"),
            ),
            FieldGroup(
                "Title сторінок",
                ("home_page_title", "apply_page_title", "archive_page_title"),
            ),
            FieldGroup(
                "Hero-колесо",
                ("wheel_prev_aria", "wheel_next_aria"),
            ),
        ),
    ),
)

SECTION_BY_ADMIN_MODEL: dict[str, ContentSection] = {
    section.admin_model_name: section for section in CONTENT_SECTIONS
}

LEGACY_SECTION_REDIRECTS: dict[tuple[str, str], tuple[str, str]] = {
    ("home", "hero-actions"): ("home", "hero"),
    ("home", "card-labels"): ("home", "calendar"),
    ("home", "stats"): ("home", "season-stats"),
    ("home", "stat-1"): ("home", "season-stats"),
    ("home", "stat-2"): ("home", "season-stats"),
    ("home", "stat-3"): ("home", "season-stats"),
    ("home", "stat-4"): ("home", "season-stats"),
    ("home", "countdown"): ("home", "calendar"),
}


def get_section(page_slug: str, section_slug: str) -> ContentSection:
    redirect = LEGACY_SECTION_REDIRECTS.get((page_slug, section_slug))
    if redirect:
        page_slug, section_slug = redirect
    for section in CONTENT_SECTIONS:
        if section.page_slug == page_slug and section.slug == section_slug:
            return section
    raise KeyError(f"Section {section_slug!r} not found on page {page_slug!r}")


def get_section_by_admin_model(admin_model_name: str) -> ContentSection:
    try:
        return SECTION_BY_ADMIN_MODEL[admin_model_name]
    except KeyError as exc:
        raise KeyError(f"Section for admin model {admin_model_name!r} not found") from exc


def get_first_section_slug(page_slug: str) -> str:
    for section in CONTENT_SECTIONS:
        if section.page_slug == page_slug:
            return section.slug
    raise KeyError(f"Page {page_slug!r} not found")


def iter_section_blocks(section: ContentSection) -> Iterator[tuple[str, str]]:
    yield from section.blocks


def all_registry_block_keys() -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    for section in CONTENT_SECTIONS:
        keys.update(section.blocks)
    return keys


def build_content_sidebar_items() -> list[dict]:
    """Плоский список секцій для sidebar «Контент сайту»."""
    return _build_sidebar_items("content")


def build_archive_sidebar_items() -> list[dict]:
    """Секції контенту для sidebar «Архів сезонів»."""
    return _build_sidebar_items("archive")


def build_season_sidebar_items() -> list[dict]:
    """Окремі сторінки для кожного з п'яти сезонів."""
    return [
        {
            "title": "Сезон «Весна»",
            "icon": "eco",
            "link": reverse_lazy("admin:tournaments_springseasontournament_changelist"),
        },
        {
            "title": "Сезон «Літо»",
            "icon": "wb_sunny",
            "link": reverse_lazy("admin:tournaments_summerseasontournament_changelist"),
        },
        {
            "title": "Сезон «Осінь»",
            "icon": "park",
            "link": reverse_lazy("admin:tournaments_autumnseasontournament_changelist"),
        },
        {
            "title": "Сезон «Зима»",
            "icon": "ac_unit",
            "link": reverse_lazy("admin:tournaments_winterseasontournament_changelist"),
        },
        {
            "title": "Сезон «Kids»",
            "icon": "child_care",
            "link": reverse_lazy("admin:tournaments_kidsseasontournament_changelist"),
        },
    ]


def _build_sidebar_items(group: str) -> list[dict]:
    return [
        {
            "title": section.sidebar_title or section.title,
            "icon": section.sidebar_icon,
            "link": reverse_lazy(
                f"admin:tournaments_{section.admin_model_name}_changelist",
            ),
        }
        for section in CONTENT_SECTIONS
        if section.sidebar_group == group
    ]
