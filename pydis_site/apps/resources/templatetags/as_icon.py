from django import template

register = template.Library()


@register.filter
def as_icon(icon: str) -> str:
    """Convert icon string in format 'type/icon' to fa-icon HTML classes."""
    icon_type, icon_name = icon.split("/")
    if icon_type.lower() == "branding":
        icon_type = "fab"
    else:
        icon_type = "fas"
    return f'{icon_type} fa-{icon_name}'
