from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone


class SiteSettings(models.Model):
    phone = models.CharField(max_length=32, default="+38 068 890 28 44", verbose_name="Телефон")
    email = models.EmailField(default="ruhcupleocup@gmail.com", verbose_name="Email")
    city = models.CharField(max_length=64, default="Львів, Україна", verbose_name="Місто")
    url_instagram = models.URLField(blank=True, verbose_name="Instagram")
    url_telegram = models.URLField(blank=True, verbose_name="Telegram")
    url_youtube = models.URLField(blank=True, verbose_name="YouTube")
    url_tiktok = models.URLField(blank=True, verbose_name="TikTok")

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

    def __str__(self) -> str:
        return "Налаштування сайту"

    @classmethod
    def load(cls) -> "SiteSettings":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Tournament(models.Model):
    class ThemeClass(models.TextChoices):
        SPRING = "theme-spring", "Весна — лайм"
        AUTUMN = "theme-autumn", "Осінь — бурштин"
        WINTER = "theme-winter", "Зима — блакитний"
        KIDS = "theme-kids", "Kids — червоний"

    class SeasonIcon(models.TextChoices):
        SPRING = "Spring", "Весна"
        AUTUMN = "Autumn", "Осінь"
        WINTER = "Winter", "Зима"
        KIDS = "Kids", "Kids"

    slug = models.SlugField(unique=True, max_length=64, verbose_name="Slug")
    title = models.CharField(max_length=64, verbose_name="Назва")
    subtitle = models.CharField(max_length=128, verbose_name="Підзаголовок")
    season = models.CharField(max_length=32, verbose_name="Сезон (UA)")
    season_en = models.CharField(
        max_length=32,
        choices=SeasonIcon.choices,
        verbose_name="Сезон (іконка)",
        help_text="Визначає іконку сезону на сайті.",
    )
    year = models.CharField(max_length=4, default="2026", verbose_name="Рік")
    theme_class = models.CharField(
        max_length=32,
        choices=ThemeClass.choices,
        verbose_name="Кольорова гама",
        help_text="Акцентний колір сторінки турніру на сайті.",
    )
    dates_display = models.CharField(max_length=128, verbose_name="Дати (текст)")
    starts_at = models.DateTimeField(verbose_name="Початок")
    ends_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Завершення",
        help_text="Після цієї дати таймер зворотного відліку не показується.",
    )
    location = models.CharField(max_length=256, verbose_name="Локація")
    match_duration_minutes = models.PositiveSmallIntegerField(
        default=20,
        verbose_name="Тривалість тайму (хв)",
        help_text="Використовується у форматі турніру на сайті.",
    )
    teams_count = models.PositiveIntegerField(verbose_name="Команд (на сайті)")
    matches_count = models.PositiveIntegerField(verbose_name="Матчів (на сайті)")
    goals_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Голів",
        help_text="Залиште порожнім, щоб приховати на сайті до внесення результатів.",
    )
    wins_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Перемог",
        help_text="Залиште порожнім, щоб приховати на сайті до внесення результатів.",
    )
    losses_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Поразок",
        help_text="Залиште порожнім, щоб приховати на сайті до внесення результатів.",
    )
    age_groups = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Вікові групи (legacy JSON)",
        help_text="Застаріле поле. Краще додавати вікові групи у вкладці нижче.",
    )
    format_text = models.CharField(max_length=128, verbose_name="Формат")
    prize = models.CharField(max_length=256, verbose_name="Нагороди")
    fee_uah = models.CharField(max_length=16, verbose_name="Внесок (₴)")
    description = models.TextField(verbose_name="Опис")
    highlight = models.CharField(max_length=256, verbose_name="Акцент")
    tagline = models.CharField(max_length=128, verbose_name="Слоган")
    icon_hint = models.CharField(max_length=64, blank=True, verbose_name="Підказка іконки")
    hero_image = models.ImageField(
        upload_to="tournaments/hero/",
        blank=True,
        verbose_name="Hero-зображення",
    )
    card_image = models.ImageField(
        upload_to="tournaments/cards/",
        blank=True,
        verbose_name="Зображення картки",
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубліковано")
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["sort_order", "starts_at"]
        verbose_name = "Турнір"
        verbose_name_plural = "Турніри"

    def __str__(self) -> str:
        return f"{self.title} · {self.season} {self.year}"

    def get_absolute_url(self) -> str:
        return reverse("tournaments:detail", kwargs={"slug": self.slug})

    @property
    def ends_at_or_starts_at(self):
        return self.ends_at or self.starts_at

    @property
    def has_ended(self) -> bool:
        return timezone.now() >= self.ends_at_or_starts_at

    @property
    def show_countdown(self) -> bool:
        return not self.has_ended

    @property
    def show_goals_stat(self) -> bool:
        return self.goals_count is not None

    @property
    def show_wins_stat(self) -> bool:
        return self.wins_count is not None

    @property
    def show_losses_stat(self) -> bool:
        return self.losses_count is not None

    @property
    def age_group_names(self) -> list[str]:
        groups = list(
            self.age_groups_rel.order_by("sort_order", "pk").values_list("name", flat=True)
        )
        return groups or self.age_groups

    @property
    def nav_label(self) -> str:
        if self.slug in ("leo-cup-autumn", "leo-cup-osen"):
            return "Leo Cup Осінь"
        if self.slug == "ruh-kids-cup":
            return "Ruh Kids"
        if self.slug == "leo-cup":
            return "Leo Cup"
        return "Ruh Cup"

    @property
    def accent_var(self) -> str:
        mapping = {
            "theme-spring": "spring",
            "theme-autumn": "autumn",
            "theme-winter": "winter",
            "theme-kids": "kids",
        }
        return mapping.get(self.theme_class, "spring")


class AgeGroup(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="age_groups_rel",
        verbose_name="Турнір",
    )
    name = models.CharField(max_length=32, verbose_name="Назва")
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Вікова група"
        verbose_name_plural = "Вікові групи"
        constraints = [
            models.UniqueConstraint(
                fields=["tournament", "name"],
                name="unique_age_group_per_tournament",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.tournament})"


class Team(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="teams",
        verbose_name="Турнір",
    )
    name = models.CharField(max_length=128, verbose_name="Назва")
    city = models.CharField(max_length=128, verbose_name="Місто")
    short_code = models.CharField(max_length=8, verbose_name="Код")
    wins = models.PositiveIntegerField(default=0, verbose_name="Перемоги")
    losses = models.PositiveIntegerField(default=0, verbose_name="Поразки")
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Команда"
        verbose_name_plural = "Команди"

    def __str__(self) -> str:
        return self.name


class Player(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="players",
        verbose_name="Команда",
    )
    age_group = models.ForeignKey(
        AgeGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="players",
        verbose_name="Вікова група",
    )
    full_name = models.CharField(max_length=128, verbose_name="Повне імʼя")
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["sort_order", "full_name"]
        verbose_name = "Гравець"
        verbose_name_plural = "Гравці"

    def __str__(self) -> str:
        return self.full_name

    @property
    def tournament(self) -> Tournament:
        return self.team.tournament


class Match(models.Model):
    class Stage(models.TextChoices):
        GROUP = "group", "Груповий етап"
        R16 = "r16", "1/8 фіналу"
        SF = "sf", "1/2 фіналу"
        FINAL = "final", "Фінал"

    class Status(models.TextChoices):
        UPCOMING = "upcoming", "Майбутній"
        LIVE = "live", "Live"
        FINISHED = "finished", "Завершено"

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="matches",
        verbose_name="Турнір",
    )
    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="home_matches",
        verbose_name="Господарі",
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="away_matches",
        verbose_name="Гості",
    )
    age_group = models.ForeignKey(
        AgeGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matches",
        verbose_name="Вікова група",
    )
    day = models.PositiveSmallIntegerField(default=1, verbose_name="День")
    time = models.TimeField(verbose_name="Час")
    field = models.CharField(max_length=64, verbose_name="Поле")
    score_home = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Голи (госп.)")
    score_away = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Голи (гості)")
    stage = models.CharField(
        max_length=16,
        choices=Stage.choices,
        default=Stage.GROUP,
        verbose_name="Етап",
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.UPCOMING,
        verbose_name="Статус",
    )

    class Meta:
        ordering = ["day", "time", "pk"]
        verbose_name = "Матч"
        verbose_name_plural = "Матчі"

    def __str__(self) -> str:
        return f"{self.home_team.short_code} — {self.away_team.short_code}"

    @property
    def time_display(self) -> str:
        return self.time.strftime("%H:%M").lstrip("0") or "0:00"


class Goal(models.Model):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name="goals",
        verbose_name="Матч",
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="goals",
        verbose_name="Гравець",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="goals",
        verbose_name="Команда",
    )
    minute = models.PositiveSmallIntegerField(verbose_name="Хвилина")

    class Meta:
        ordering = ["minute", "pk"]
        verbose_name = "Гол"
        verbose_name_plural = "Голи"

    def __str__(self) -> str:
        scorer = self.player.full_name if self.player else "—"
        return f"{scorer} ({self.minute}′)"


class ArchiveEdition(models.Model):
    year = models.CharField(max_length=4, verbose_name="Рік")
    title = models.CharField(max_length=64, verbose_name="Назва")
    season = models.CharField(max_length=32, verbose_name="Сезон")
    theme_class = models.CharField(
        max_length=32,
        choices=Tournament.ThemeClass.choices,
        verbose_name="Кольорова гама",
    )
    teams_count = models.PositiveIntegerField(verbose_name="Команд")
    matches_count = models.PositiveIntegerField(verbose_name="Матчів")
    goals_count = models.PositiveIntegerField(verbose_name="Голів")
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")
    is_published = models.BooleanField(default=True, verbose_name="Опубліковано")

    class Meta:
        ordering = ["-year", "sort_order", "pk"]
        verbose_name = "Архівний турнір"
        verbose_name_plural = "Архівні турніри"

    def __str__(self) -> str:
        return f"{self.title} · {self.season} {self.year}"


class GalleryImage(models.Model):
    class Height(models.IntegerChoices):
        SHORT = 240, "240 px"
        TALL = 320, "320 px"

    image = models.ImageField(upload_to="gallery/", verbose_name="Зображення")
    alt_text = models.CharField(max_length=256, verbose_name="Alt-текст")
    label = models.CharField(max_length=128, blank=True, verbose_name="Підпис")
    height = models.PositiveSmallIntegerField(
        choices=Height.choices,
        default=Height.SHORT,
        verbose_name="Висота блоку",
    )
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")
    show_on_home = models.BooleanField(default=False, verbose_name="На головній")
    show_on_archive = models.BooleanField(default=True, verbose_name="В архіві")

    class Meta:
        ordering = ["sort_order", "pk"]
        verbose_name = "Зображення галереї"
        verbose_name_plural = "Галерея"

    def __str__(self) -> str:
        return self.label or self.alt_text


class Application(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Нова"
        PROCESSED = "processed", "Оброблена"

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.PROTECT,
        related_name="applications",
        verbose_name="Турнір",
    )
    phone = models.CharField(max_length=32, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    team_name = models.CharField(max_length=256, verbose_name="Назва команди")
    age_category = models.CharField(max_length=128, verbose_name="Вікова категорія")
    coach_name = models.CharField(max_length=128, blank=True, verbose_name="Тренер")
    city = models.CharField(max_length=128, blank=True, verbose_name="Місто")
    players_count = models.PositiveSmallIntegerField(default=12, verbose_name="Кількість гравців")
    note = models.TextField(blank=True, verbose_name="Примітка")
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self) -> str:
        return f"{self.team_name} → {self.tournament}"

    def send_notification(self) -> None:
        subject = f"Нова заявка: {self.team_name} — {self.tournament}"
        body = (
            f"Турнір: {self.tournament}\n"
            f"Команда: {self.team_name}\n"
            f"Вікова категорія: {self.age_category}\n"
            f"Тренер: {self.coach_name or '—'}\n"
            f"Місто: {self.city or '—'}\n"
            f"Гравців: {self.players_count}\n"
            f"Телефон: {self.phone}\n"
            f"Email: {self.email}\n"
            f"Примітка: {self.note or '—'}\n"
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.APPLICATION_NOTIFY_EMAIL],
            fail_silently=False,
        )
