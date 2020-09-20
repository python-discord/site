import os
from datetime import datetime
from typing import Optional

import yaml
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View
from markdown import Markdown


class GuideView(View):
    """Shows specific guide page."""

    def get(self, request: WSGIRequest, guide: str, category: Optional[str] = None) -> HttpResponse:
        """Collect guide content and display it. When guide don't exist, return 404."""
        if category is None:
            path = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "resources", "guides", f"{guide}.md")
            category_name = None
        else:
            dir_path = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "resources", "guides", category)
            path = os.path.join(dir_path, f"{guide}.md")
            with open(os.path.join(dir_path, "_info.yml")) as f:
                category_name = yaml.load(f.read())["name"]

        if not os.path.exists(path) or not os.path.isfile(path):
            raise Http404(f"Guide not found {path}")

        md = Markdown(extensions=['meta', 'attr_list'])
        with open(path) as f:
            html = md.convert(f.read())
            f.close()

        category_data = {
            "title": category_name,
            "name": category,
        }

        return render(
            request,
            "guides/guide.html",
            {
                "guide": html,
                "metadata": md.Meta,
                "last_modified": datetime.fromtimestamp(os.path.getmtime(path)).strftime("%dth %B %Y"),
                "relevant_links": {
                    link: value for link, value in zip(
                        md.Meta.get("relevantlinks", []),
                        md.Meta.get("relevantlinkvalues", [])
                    )
                },
                "category_data": category_data,
            }
        )
