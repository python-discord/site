from django.views.generic import TemplateView

    
class ResourcesView(TemplateView):
    """View for resources index page."""

    template_name = "resources/resources.html"
