from django import template

register = template.Library()


@register.filter
def starts_with(value: str, arg: str):
    """
    Simple filter for checking if a string value starts with another string.

    Kind of surprising that Django doesn't come with this one, actually...

    Usage:

    ```django
        {% if request.url | starts_with:"/wiki" %}
          ...
        {% endif %}
    ```
    """

    return value.startswith(arg)
