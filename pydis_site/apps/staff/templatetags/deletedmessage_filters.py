from datetime import datetime

from django import template

register = template.Library()


@register.filter
def hex_colour(color: int) -> str:
    """Converts an integer representation of a colour to the RGB hex value."""
    return f"#{color:0>6X}"


@register.filter
def footer_datetime(timestamp: str) -> datetime:
    """Takes an embed timestamp and returns a timezone-aware datetime object."""
    return datetime.fromisoformat(timestamp)
