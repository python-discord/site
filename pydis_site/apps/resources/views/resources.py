from django.views.generic import TemplateView
from django.shortcuts import render

# class ResourcesView(TemplateView):
#     """View for resources index page."""
#
#     template_name = "resources/resources.html"


def resource_view(request):
    return render(request, template_name="resources/resources.html")
