from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from pydis_site.apps.guides.utils import get_categories, get_guides


class GuidesView(View):
    """Shows all guides and categories."""

    def get(self, request: WSGIRequest) -> HttpResponse:
        """Shows all guides and categories."""
        return render(request, "guides/guides.html", {"guides": get_guides(), "categories": get_categories()})
