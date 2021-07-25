from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from pydis_site.apps.resources.utils import get_resources_meta

RESOURCE_META_TAGS = get_resources_meta()


def format_checkbox_options(options: str) -> list[str]:
    """Split up the comma separated parameters into a list."""
    return options.split(",")[:-1] if options else []


def resource_view(request: HttpRequest) -> HttpResponse:
    """View for resources index page."""
    return render(
        request,
        template_name="resources/resources.html",
        context={
            "checkboxOptions": format_checkbox_options(request.GET.get("checkboxOptions")),
            "topics": RESOURCE_META_TAGS.get("topics"),
            "tag_types": RESOURCE_META_TAGS.get("type"),
            "payment_tiers": RESOURCE_META_TAGS.get("payment_tiers"),
            "complexities": RESOURCE_META_TAGS.get("complexity")
        }
    )
