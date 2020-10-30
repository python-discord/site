from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from pydis_site.apps.content.utils import get_article, get_category, get_github_information


class ArticleView(TemplateView):
    """Shows specific guide page."""

    template_name = "content/article.html"

    def get_context_data(self, **kwargs):
        """Add custom context info about article."""
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get("category")
        article_result = get_article(self.kwargs["article"], category)

        if category is not None:
            category_data = get_category(category)
            category_data["raw_name"] = category
        else:
            category_data = {"name": None, "raw_name": None}

        context["article"] = article_result
        context["category_data"] = category_data
        context["relevant_links"] = {
            link: value for link, value in zip(
                article_result["metadata"].get("relevant_links", "").split(","),
                article_result["metadata"].get("relevant_link_values", "").split(",")
            ) if link != "" and value != ""
        }
        context["github_data"] = get_github_information(self.kwargs["article"], category)
        return context
