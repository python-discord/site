import os

import yaml
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from markdown import Markdown


class GuidesView(View):
    """Shows all guides and categories."""

    def get(self, request: WSGIRequest) -> HttpResponse:
        """Shows all guides and categories."""
        guides = {}
        categories = {}

        guides_path = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "resources", "guides")
        for name in os.listdir(guides_path):
            full_path = os.path.join(guides_path, name)
            if os.path.isdir(full_path):
                with open(os.path.join(full_path, "_info.yml")) as f:
                    category = yaml.load(f.read())

                categories[name] = {"name": category["name"], "description": category["description"]}
            elif os.path.isfile(full_path) and name.endswith(".md"):
                md = Markdown(extensions=['meta'])
                with open(full_path) as f:
                    md.convert(f.read())

                guides[os.path.splitext(name)[0]] = {
                    "name": md.Meta["title"],
                    "short_description": md.Meta["shortdescription"]
                }

        return render(request, "guides/guides.html", {"guides": guides, "categories": categories})
