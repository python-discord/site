from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class ResourcesView(View):
    """Handles base resources page that shows different resource types."""

    def get(self, request: WSGIRequest) -> HttpResponse:
        """Show base resources page."""
        return render(request, "resources/resources.html")
