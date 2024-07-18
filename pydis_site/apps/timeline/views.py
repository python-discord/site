from django.apps import apps
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

APP_NAME = "timeline"

class TimelineView(View):
    """A vertical timeline showcasing milestones in the history of Python Discord."""

    def get(self, request: WSGIRequest) -> HttpResponse:
        """Render the timeline."""
        app = apps.get_app_config(APP_NAME)

        return render(
            request,
            template_name="timeline/timeline.html",
            context={ "entries": app.entries },
        )
