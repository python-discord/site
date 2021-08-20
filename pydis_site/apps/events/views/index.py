from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Events index page view."""

    template_name = "events/index.html"
