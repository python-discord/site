from django.db.models.query import QuerySet
from django.views.generic.list import ListView

from pydis_site.apps.api.models.bot.tag import Tag


class ListView(ListView):
    """A Tag list view to display all the tags."""

    model = Tag
    template_name = "home/tags/tag_list.html"

    def get_queryset(self) -> QuerySet:
        """Return Tag objects ordered by the title field."""
        queryset = Tag.objects.all().order_by("title")
        return queryset
