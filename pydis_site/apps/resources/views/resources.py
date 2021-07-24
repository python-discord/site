from django.shortcuts import render

from pydis_site.apps.resources.utils import get_resources_meta

RESOURCE_META_TAGS = get_resources_meta()


def format_checkbox_options(options: str) -> list:
    """Split up the comma separated parameters into a list."""
    if options:
        return options.split(",")[:-1]
    return list()


def resource_view(request):
    """View for resources index page."""
    context = {
        "checkboxOptions": format_checkbox_options(request.GET.get("checkboxOptions")),
        "topics": RESOURCE_META_TAGS.get("topics"),
        "tag_types": RESOURCE_META_TAGS.get("type"),
        "payment_tiers": RESOURCE_META_TAGS.get("payment_tiers"),
        "complexities": RESOURCE_META_TAGS.get("complexity")
    }
    return render(request, template_name="resources/resources.html", context=context)
