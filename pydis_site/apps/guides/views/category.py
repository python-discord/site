import os

import yaml
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View
from markdown import Markdown


class CategoryView(View):
    """Handles guides category page."""

    def get(self, request: WSGIRequest, category: str) -> HttpResponse:
        """Handles page that displays category guides."""
        path = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "resources", "guides", category)
        if not os.path.exists(path) or not os.path.isdir(path):
            raise Http404("Category not found.")

        with open(os.path.join(path, "_info.yml")) as f:
            category_info = yaml.load(f.read())

        guides = {}

        for filename in os.listdir(path):
            if filename.endswith(".md"):
                md = Markdown(extensions=["meta"])
                with open(os.path.join(path, filename)) as f:
                    md.convert(f.read())

                guides[os.path.splitext(filename)[0]] = {
                    "title": md.Meta["title"],
                    "short_description": md.Meta["shortdescription"]
                }

        return render(
            request,
            "guides/category.html",
            {"category_info": category_info, "guides": guides, "category_name": category}
        )
