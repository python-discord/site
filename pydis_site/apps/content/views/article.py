from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from pydis_site.apps.content.utils import get_article, get_category


class ArticleView(View):
    """Shows specific guide page."""

    def get(
            self,
            request: WSGIRequest,
            article: str,
            category: Optional[str] = None
    ) -> HttpResponse:
        """Collect guide content and display it. When guide don't exist, return 404."""
        article_result = get_article(article, category)

        if category is not None:
            category_data = get_category(category)
            category_data["raw_name"] = category
        else:
            category_data = {"name": None, "raw_name": None}

        relevant_links = {
            link: value for link, value in zip(
                article_result["metadata"].get("relevant_links", "").split(","),
                article_result["metadata"].get("relevant_link_values", "").split(",")
            )
        }

        if relevant_links == {"": ""}:
            relevant_links = {}

        return render(
            request,
            "content/article.html",
            {
                "article": article_result,
                "category_data": category_data,
                "relevant_links": relevant_links
            }
        )
