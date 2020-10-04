import os
from datetime import datetime
from typing import Optional

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from pydis_site.apps.content.utils import get_category, get_article


class ArticleView(View):
    """Shows specific guide page."""

    def get(self, request: WSGIRequest, article: str, category: Optional[str] = None) -> HttpResponse:
        """Collect guide content and display it. When guide don't exist, return 404."""
        article_result = get_article(article, category)

        if category is not None:
            path = os.path.join(
                settings.BASE_DIR, "pydis_site", "apps", "content", "resources", "content", category, f"{article}.md"
            )
        else:
            path = os.path.join(
                settings.BASE_DIR, "pydis_site", "apps", "content", "resources", "content", f"{article}.md"
            )

        if category is not None:
            category_data = get_category(category)
            category_data["raw_name"] = category
        else:
            category_data = {"name": None, "raw_name": None}

        return render(
            request,
            "content/article.html",
            {
                "article": article_result,
                "last_modified": datetime.fromtimestamp(os.path.getmtime(path)).strftime("%dth %B %Y"),
                "category_data": category_data,
                "relevant_links": {
                    link: value for link, value in zip(
                        article_result["metadata"].get("relevantlinks", []),
                        article_result["metadata"].get("relevantlinkvalues", [])
                    )
                }
            }
        )
