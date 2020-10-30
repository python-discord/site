from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from pydis_site.apps.content.utils import get_articles, get_category


class CategoryView(TemplateView):
    """Handles content category page."""

    template_name = "content/category.html"

    def get_context_data(self, **kwargs):
        """Add category data to context."""
        context = super().get_context_data(**kwargs)
        context["category_info"] = get_category(self.kwargs["category"])
        context["content"] = get_articles(self.kwargs["category"])
        context["category_name"] = self.kwargs["category"]
        return context
