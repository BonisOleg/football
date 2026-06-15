import re
from urllib.parse import urlparse

from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError

from src.tournaments.admin_guidelines import IMAGE_PROFILES, TEXT_MAX_LENGTHS, format_file_size
from src.tournaments.utils.block_render import _vimeo_id, _youtube_id
from src.tournaments.utils.html import sanitize_html

FORBIDDEN_HTML_PATTERNS = (
    re.compile(r"<\s*script\b", re.IGNORECASE),
    re.compile(r"<\s*style\b", re.IGNORECASE),
    re.compile(r"<\s*iframe\b", re.IGNORECASE),
    re.compile(r"<\s*img\b", re.IGNORECASE),
    re.compile(r"<\s*video\b", re.IGNORECASE),
    re.compile(r"<\s*object\b", re.IGNORECASE),
    re.compile(r"<\s*embed\b", re.IGNORECASE),
    re.compile(r"\bon\w+\s*=", re.IGNORECASE),
    re.compile(r"style\s*=", re.IGNORECASE),
)

ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP", "GIF"}


def validate_image_upload(file, profile: str) -> None:
    if file is None:
        return

    spec = IMAGE_PROFILES[profile]
    size = getattr(file, "size", None)
    if size is None:
        return

    if size > spec.max_bytes:
        raise ValidationError(
            f"Фото занадто велике ({format_file_size(size)}). "
            f"Максимум {format_file_size(spec.max_bytes)}. "
            "Стисніть зображення перед завантаженням."
        )

    try:
        file.seek(0)
        image = Image.open(file)
        image.verify()
        file.seek(0)
        image = Image.open(file)
        width, height = image.size
        image_format = (image.format or "").upper()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValidationError("Файл не є коректним зображенням. Завантажте JPG, WebP або PNG.") from exc
    finally:
        file.seek(0)

    if image_format and image_format not in ALLOWED_IMAGE_FORMATS:
        raise ValidationError(
            f"Формат {image_format} не підтримується. Дозволено: {spec.formats}."
        )

    if spec.min_width and width < spec.min_width:
        raise ValidationError(
            f"Ширина зображення занадто мала ({width} px). "
            f"Мінімум {spec.min_width} px. Рекомендовано {spec.recommended}."
        )

    if spec.max_width and width > spec.max_width:
        raise ValidationError(
            f"Ширина зображення занадто велика ({width} px). "
            f"Максимум {spec.max_width} px. Рекомендовано {spec.recommended}."
        )

    if spec.max_height and height > spec.max_height:
        raise ValidationError(
            f"Висота зображення занадто велика ({height} px). "
            f"Максимум {spec.max_height} px. Рекомендовано {spec.recommended}."
        )


def validate_rich_text(
    html: str,
    *,
    field_key: str,
    allow_accent_span: bool = False,
) -> str:
    value = (html or "").strip()
    if not value:
        return value

    max_length = TEXT_MAX_LENGTHS.get(field_key)
    if max_length and len(value) > max_length:
        raise ValidationError(
            f"Текст занадто довгий ({len(value)} символів). Максимум {max_length}."
        )

    for pattern in FORBIDDEN_HTML_PATTERNS:
        if pattern.search(value):
            raise ValidationError(
                "Текст містить заборонений HTML (скрипти, стилі, картинки або відео). "
                "Використовуйте лише форматування редактора: жирний, курсив, списки, посилання."
            )

    if not allow_accent_span and re.search(
        r"<\s*span\b[^>]*class\s*=\s*['\"]?text-accent",
        value,
        re.IGNORECASE,
    ):
        raise ValidationError(
            'Тег <span class="text-accent"> дозволений лише в заголовках з акцентом '
            "(stats_title, hero_title, editions_title, gallery_title)."
        )

    cleaned = sanitize_html(value)
    if _meaningful_text(cleaned) != _meaningful_text(value):
        raise ValidationError(
            "Частина HTML буде видалена на сайті і може зламати блок. "
            "Приберіть зайві теги, стилі та вставки з Word."
        )

    return cleaned


def validate_plain_text(value: str, field_key: str) -> str:
    text = (value or "").strip()
    if not text:
        return text

    max_length = TEXT_MAX_LENGTHS.get(field_key)
    if max_length and len(text) > max_length:
        raise ValidationError(
            f"Текст занадто довгий ({len(text)} символів). Максимум {max_length}."
        )

    if "<" in text or ">" in text:
        raise ValidationError(
            "Поле приймає лише звичайний текст без HTML. "
            "Приберіть теги <…> — вони можуть зламати верстку."
        )

    return text


def validate_video_url(url: str) -> str:
    value = (url or "").strip()
    if not value:
        return value

    parsed = urlparse(value)
    host = (parsed.netloc or "").lower().replace("www.", "")

    if host in {"youtube.com", "youtu.be", "m.youtube.com"} and _youtube_id(value, parsed):
        return value

    if host in {"vimeo.com", "player.vimeo.com"} and _vimeo_id(parsed):
        return value

    raise ValidationError(
        "Дозволені лише посилання YouTube або Vimeo. "
        "Приклад: https://www.youtube.com/watch?v=… або https://vimeo.com/123456789"
    )


def _meaningful_text(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html or "")
    return re.sub(r"\s+", " ", text).strip()
