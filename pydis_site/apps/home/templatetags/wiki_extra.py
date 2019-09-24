from typing import Any, Dict, List, Type, Union

from django import template
from django.forms import BooleanField, BoundField, CharField, Field, ImageField, ModelChoiceField
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import SafeText, mark_safe
from wiki.editors.markitup import MarkItUpWidget
from wiki.forms import WikiSlugField
from wiki.models import URLPath
from wiki.plugins.notifications.forms import SettingsModelChoiceField

TEMPLATE_PATH = "wiki/forms/fields/{0}.html"

TEMPLATES: Dict[Type, str] = {
    BooleanField: TEMPLATE_PATH.format("boolean"),
    CharField: TEMPLATE_PATH.format("char"),
    ImageField: TEMPLATE_PATH.format("image"),

    ModelChoiceField: TEMPLATE_PATH.format("model_choice"),
    SettingsModelChoiceField: TEMPLATE_PATH.format("model_choice"),
    WikiSlugField: TEMPLATE_PATH.format("wiki_slug_render"),
}


register = template.Library()


def get_unbound_field(field: Union[BoundField, Field]) -> Field:
    """
    Unwraps a bound Django Forms field, returning the unbound field.

    Bound fields often don't give you the same level of access to the field's underlying attributes,
    so sometimes it helps to have access to the underlying field object.
    """
    while isinstance(field, BoundField):
        field = field.field

    return field


def render(template_path: str, context: Dict[str, Any]) -> SafeText:
    """
    Renders a template at a specified path, with the provided context dictionary.

    This was extracted mostly for the sake of mocking it out in the tests - but do note that
    the resulting rendered template is wrapped with `mark_safe`, so it will not be escaped.
    """
    return mark_safe(get_template(template_path).render(context))  # noqa: S703, S308


@register.simple_tag
def render_field(field: Field, render_labels: bool = True) -> SafeText:
    """
    Renders a form field using a custom template designed specifically for the wiki forms.

    As the wiki uses custom form rendering logic, we were unable to make use of Crispy Forms for
    it. This means that, in order to customize the form fields, we needed to be able to render
    the fields manually. This function handles that logic.

    Sometimes we don't want to render the label that goes with a field - the `render_labels`
    argument defaults to True, but can be set to False if the label shouldn't be rendered.

    The label rendering logic is left up to the template.

    Usage: `{% render_field field_obj [render_labels=True/False] %}`
    """
    unbound_field = get_unbound_field(field)

    if not isinstance(render_labels, bool):
        render_labels = True

    template_path = TEMPLATES.get(unbound_field.__class__, TEMPLATE_PATH.format("in_place_render"))
    is_markitup = isinstance(unbound_field.widget, MarkItUpWidget)
    context = {"field": field, "is_markitup": is_markitup, "render_labels": render_labels}

    return render(template_path, context)


@register.simple_tag(takes_context=True)
def get_field_options(context: Context, field: BoundField) -> str:
    """
    Retrieves the field options for a multiple choice field, and stores it in the context.

    This tag exists because we can't call functions within Django templates directly, and is
    only made use of in the template for ModelChoice (and derived) fields - but would work fine
    with anything that makes use of your standard `<select>` element widgets.

    This stores the parsed options under `options` in the context, which will subsequently
    be available in the template.

    Usage:

    ```django
    {% get_field_options field_object %}

    {% if options %}
      {% for group_name, group_choices, group_index in options %}
        ...
      {% endfor %}
    {% endif %}
    ```
    """
    widget = field.field.widget

    if field.value() is None:
        value: List[str] = []
    else:
        value = [str(field.value())]

    context["options"] = widget.optgroups(field.name, value)
    return ""


@register.filter
def render_urlpath(value: Union[URLPath, str]) -> str:
    """
    Simple filter to render a URLPath (or string) into a template.

    This is used where the wiki intends to render a path - mostly because if you just
    `str(url_path)`, you'll actually get a path that starts with `(root)` instead of `/`.

    We support strings here as well because the wiki is very inconsistent about when it
    provides a string versus when it provides a URLPath, and it was too much work to figure out
    and account for it in the templates.

    Usage: `{{ url_path | render_urlpath }}`
    """
    if isinstance(value, str):
        return value or "/"

    return value.path or "/"
