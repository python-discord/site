from django import template

register = template.Library()


@register.filter
def starts_with(value: str, arg: str):
    return value.startswith(arg)
