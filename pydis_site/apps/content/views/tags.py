import re

import frontmatter
import markdown
from django.conf import settings
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView

from pydis_site.apps.content import utils
from pydis_site.apps.content.models import Tag

COMMAND_REGEX = re.compile(r"`*!tags? (?P<name>[\w\d-]+)`*")


class TagView(TemplateView):
    """Handles tag pages."""

    template_name = "content/tag.html"

    def get_context_data(self, **kwargs) -> dict:
        """Get the relevant context for this tag page."""
        try:
            tag = utils.get_tag(kwargs.get("name"))
        except Tag.DoesNotExist:
            raise Http404

        context = super().get_context_data(**kwargs)
        context["page_title"] = tag.name
        body = frontmatter.parse(tag.body)
        content = body[1]

        # Check for tags which can be hyperlinked
        start = 0
        while match := COMMAND_REGEX.search(content, start):
            link = reverse("content:tag", kwargs={"name": match.group("name")})
            content = content[:match.start()] + f"[{match.group()}]({link})" + content[match.end():]
            start = match.end()

        # Add support for some embed elements
        if embed := body[0].get("embed"):
            context["page_title"] = embed["title"]
            if image := embed.get("image"):
                content = f"![{embed['title']}]({image['url']})\n\n" + content

        context.update({
            "page": markdown.markdown(content, extensions=["pymdownx.superfences"]),
            "tag": tag,
        })

        context["breadcrumb_items"] = [{
            "name": utils.get_category(settings.CONTENT_PAGES_PATH / location)["title"],
            "path": str(location)
        } for location in [".", "tags"]]

        return context
