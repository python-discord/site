from datetime import datetime

from django import template

register = template.Library()


@register.filter
def hex_colour(color: int) -> str:
    """
    Converts an integer representation of a colour to the RGB hex value.

    As we are using a Discord dark theme analogue, black colours are returned as white instead.
    """
    colour = f"#{color:0>6X}"
    return colour if colour != "#000000" else "#FFFFFF"


@register.filter
def footer_datetime(timestamp: str) -> datetime:
    """Takes an embed timestamp and returns a timezone-aware datetime object."""
    return datetime.fromisoformat(timestamp)


@register.filter
def visible_newlines(text: str) -> str:
    """Takes an embed timestamp and returns a timezone-aware datetime object."""
    return text.replace("\n", " <span class='has-text-grey'>↵</span><br>")
