from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from pydis_site.apps.guides.utils import get_category, get_guides


class CategoryView(View):
    """Handles guides category page."""

    def get(self, request: WSGIRequest, category: str) -> HttpResponse:
        """Handles page that displays category guides."""
        return render(
            request,
            "guides/category.html",
            {"category_info": get_category(category), "guides": get_guides(category), "category_name": category}
        )
