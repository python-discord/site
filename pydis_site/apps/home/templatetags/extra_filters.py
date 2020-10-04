from django import template

register = template.Library()


@register.filter
def starts_with(value: str, arg: str) -> bool:
    """
    Simple filter for checking if a string value starts with another string.

    Usage:

    ```django
        {% if request.url | starts_with:"/events" %}
          ...
        {% endif %}
    ```
    """
    return value.startswith(arg)
