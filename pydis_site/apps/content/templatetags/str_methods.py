from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def replace_hyphens(value: str, replacement: str) -> str:
    """
    Simple filter to replace hyphens with the specified replacement string.

    Usage:

    ```django
        {% for name_with_hyphens in name_list %}
            {{ name_with_hyphens|replace_hyphen:" " }}
        {% endfor %}
    ```
    """
    return value.replace("-", replacement)
