from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from pydis_site.apps.content.utils import get_articles, get_categories


class ArticlesView(TemplateView):
    """Shows all content and categories."""

    template_name = "content/articles.html"

    def get_context_data(self, **kwargs):
        """Add articles and categories data to template context."""
        context = super().get_context_data(**kwargs)
        context["content"] = get_articles()
        context["categories"] = get_categories()
        return context
