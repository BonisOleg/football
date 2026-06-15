import bleach

ALLOWED_TAGS = ["p", "br", "strong", "em", "a", "ul", "ol", "li", "span"]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "rel", "target"],
    "span": ["class"],
}


def _attribute_filter(tag: str, name: str, value: str) -> bool:
    if tag == "span" and name == "class":
        return value.strip() == "text-accent"
    allowed = ALLOWED_ATTRIBUTES.get(tag, [])
    return name in allowed


def sanitize_html(value: str) -> str:
    if not value:
        return ""
    return bleach.clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=_attribute_filter,
        strip=True,
    )
