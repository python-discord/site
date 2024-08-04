import json

from django.apps import apps
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views import View


APP_NAME = "resources"


class ResourceView(View):
    """Our curated list of good learning resources."""

    def get(self, request: WSGIRequest, resource_type: str | None = None) -> HttpResponse:
        """List out all the resources, and any filtering options from the URL."""
        # Add type filtering if the request is made to somewhere like /resources/video.
        # We also convert all spaces to dashes, so they'll correspond with the filters.

        app = apps.get_app_config(APP_NAME)

        if resource_type:
            dashless_resource_type = resource_type.replace("-", " ")

            if dashless_resource_type.title() not in app.filters["Type"]["filters"]:
                return HttpResponseNotFound()

            resource_type = resource_type.replace(" ", "-")

        return render(
            request,
            template_name="resources/resources.html",
            context={
                "resources": app.resources,
                "filters": app.filters,
                "valid_filters": json.dumps(app.valid_filters),
                "resource_type": resource_type,
            }
        )


class ResourceFilterView(View):
    """Exposes resource filters for the bot."""

    def get(self, request: WSGIRequest) -> HttpResponse:
        """Return resource filters as JSON."""
        app = apps.get_app_config(APP_NAME)
        return JsonResponse(app.valid_filters)
