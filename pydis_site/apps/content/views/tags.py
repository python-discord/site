import re
import typing

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

    tag: typing.Union[Tag, list[Tag]]
    is_group: bool

    def setup(self, *args, **kwargs) -> None:
        """Look for a tag, and configure the view."""
        super().setup(*args, **kwargs)

        try:
            self.tag = utils.get_tag(kwargs.get("location"))
            self.is_group = isinstance(self.tag, list)
        except Tag.DoesNotExist:
            raise Http404

    def get_template_names(self) -> list[str]:
        """Either return the tag page template, or the listing."""
        if self.is_group:
            template_name = "content/listing.html"
        else:
            template_name = "content/tag.html"

        return [template_name]

    def get_context_data(self, **kwargs) -> dict:
        """Get the relevant context for this tag page or group."""
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [{
            "name": utils.get_category(settings.CONTENT_PAGES_PATH / location)["title"],
            "path": location,
        } for location in (".", "tags")]

        if self.is_group:
            self._set_group_context(context, self.tag)
        else:
            self._set_tag_context(context, self.tag)

        return context

    @staticmethod
    def _set_tag_context(context: dict[str, any], tag: Tag) -> None:
        """Update the context with the information for a tag page."""
        context.update({
            "page_title": tag.name,
            "tag": tag,
        })

        if tag.group:
            # Add group names to the breadcrumbs
            context["breadcrumb_items"].append({
                "name": tag.group,
                "path": f"tags/{tag.group}",
            })

        # Clean up tag body
        body = frontmatter.parse(tag.body)
        content = body[1]

        # Check for tags which can be hyperlinked
        def sub(match: re.Match) -> str:
            link = reverse("content:tag", kwargs={"location": match.group("name")})
            return f"[{match.group()}]({link})"
        content = COMMAND_REGEX.sub(sub, content)

        # Add support for some embed elements
        if embed := body[0].get("embed"):
            context["page_title"] = embed["title"]
            if image := embed.get("image"):
                content = f"![{embed['title']}]({image['url']})\n\n" + content

        # Insert the content
        context["page"] = markdown.markdown(content, extensions=["pymdownx.superfences"])

    @staticmethod
    def _set_group_context(context: dict[str, any], tags: list[Tag]) -> None:
        """Update the context with the information for a group of tags."""
        group = tags[0].group
        context.update({
            "categories": {},
            "pages": utils.get_tag_category(tags, collapse_groups=False),
            "page_title": group,
            "icon": "fab fa-tags",
            "is_tag_listing": True,
            "app_name": "content:tag",
            "path": f"{group}/",
            "tag_url": f"{tags[0].URL_BASE}/{group}"
        })
