from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from pydis_site.apps.resources.resource_search import RESOURCE_TABLE, get_resources_from_search

RESOURCE_META_TAGS = {k: set(v) for k, v in RESOURCE_TABLE.items()}


def _parse_checkbox_options(options: str) -> set[str]:
    """Split up the comma separated query parameters for checkbox options into a list."""
    return set(options.split(",")[:-1])


def resource_view(request: HttpRequest) -> HttpResponse:
    """View for resources index page."""
    checkbox_options = {
        a: _parse_checkbox_options(request.GET.get(b))
        for a, b in (
            ('topics', 'topic'),
            ('type', 'type'),
            ('payment_tiers', 'payment'),
            ('complexity', 'complexity'),
        )
    }

    topics = sorted(RESOURCE_META_TAGS.get("topics"))

    return render(
        request,
        template_name="resources/resources.html",
        context={
            "checkboxOptions": checkbox_options,
            "topics_1": topics[:len(topics) // 2],
            "topics_2": topics[len(topics) // 2:],
            "tag_types": sorted(RESOURCE_META_TAGS.get("type")),
            "payment_tiers": sorted(RESOURCE_META_TAGS.get("payment_tiers")),
            "complexities": sorted(RESOURCE_META_TAGS.get("complexity")),
            "resources": get_resources_from_search(checkbox_options)
        }
    )
