from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from pydis_site.apps.content.utils import get_category, get_articles


class CategoryView(View):
    """Handles content category page."""

    def get(self, request: WSGIRequest, category: str) -> HttpResponse:
        """Handles page that displays category content."""
        return render(
            request,
            "content/category.html",
            {"category_info": get_category(category), "content": get_articles(category), "category_name": category}
        )
