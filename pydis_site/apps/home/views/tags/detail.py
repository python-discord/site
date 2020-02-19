import logging
from typing import Union

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.detail import DetailView

from pydis_site.apps.api.models.bot.tag import Tag


logger = logging.getLogger(__name__)


class DetailView(DetailView):
    """Tags detail view, to view the entier tag embed."""

    model = Tag
    template_name = "home/tags/tag_detail.html"

    def get_object(self, *args, **kwargs) -> Union[Tag, HttpResponse]:
        """Get Tag model obejct using the title or show 404 page if object does not exist."""
        title = self.kwargs.get("title")
        return get_object_or_404(Tag, title=title)

    def get_context_data(self, *args, **kwargs) -> dict:
        """Make the context dictionary."""
        context = super().get_context_data(**kwargs)

        first_tag = Tag.objects.first().title
        last_tag = Tag.objects.last().title

        context['first_tag'] = first_tag
        context['last_tag'] = last_tag

        return context

    def post(self, *args, **kwargs) -> HttpResponse:
        """HTTP POST: Used to display the next/prev Tag detail page."""
        # button_info has the name and value options given to the button element in the HTML page.
        # The first index contains the name and value.
        button_info = list(self.request.POST.items())[1]

        # Button name has 2 values: next or prev.
        # This indicates whether to send the next page or prev page.
        button_name = button_info[0]
        current_tag = button_info[1]

        all_tags = Tag.objects.all().order_by("title")

        tag_titles = [tag.title for tag in all_tags]
        current_index = tag_titles.index(current_tag)

        if button_name == "next":
            if current_index + 1 == len(tag_titles):
                tag_to_display = tag_titles[0]
            else:
                tag_to_display = tag_titles[current_index+1]
        else:
            tag_to_display = tag_titles[current_index-1]

        """
        The below line is required or else the `get_context_data()` method will fail
        when ever there is a post request.

        Reason:
        The source code for `get_context_data()` uses self.object declared in `get_object()`.
        When a POST request, the `get_object()` is not being called hence the below code.
        """
        obj = Tag.objects.get(title=tag_to_display)
        self.object = obj

        context = self.get_context_data()

        return render(self.request, self.template_name, context)
