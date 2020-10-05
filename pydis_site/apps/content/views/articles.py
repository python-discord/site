from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from pydis_site.apps.content.utils import get_articles, get_categories


class ArticlesView(View):
    """Shows all content and categories."""

    def get(self, request: WSGIRequest) -> HttpResponse:
        """Shows all content and categories."""
        return render(
            request,
            "content/articles.html",
            {"content": get_articles(), "categories": get_categories()}
        )
