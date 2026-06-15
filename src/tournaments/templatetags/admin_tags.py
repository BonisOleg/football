from django import template

register = template.Library()


@register.simple_tag(name="has_nav_item_active_deep")
def has_nav_item_active_deep(items) -> bool:
    if not isinstance(items, list):
        return False
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("active"):
            return True
        nested = item.get("items")
        if isinstance(nested, list) and has_nav_item_active_deep(nested):
            return True
    return False
