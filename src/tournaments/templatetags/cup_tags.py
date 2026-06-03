from django import template

register = template.Library()


@register.filter
def split(value: str, arg: str = " ") -> list:
    return value.split(arg)


@register.filter
def pad02(value: int) -> str:
    return str(value).zfill(2)
