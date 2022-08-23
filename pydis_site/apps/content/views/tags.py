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

# The following regex tries to parse a tag command
# It'll read up to two words seperated by spaces
# If the command does not include a group, the tag name will be in the `first` group
# If there's a second word after the command, or if there's a tag group, extra logic
# is necessary to determine whether it's a tag with a group, or a tag with text after it
COMMAND_REGEX = re.compile(r"`*!tags? (?P<first>[\w-]+)(?P<second> [\w-]+)?`*")


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
            first, second = match.groups()
            location = first
            text, extra = match.group(), ""

            if second is not None:
                # Possibly a tag group
                try:
                    new_location = f"{first}/{second.strip()}"
                    utils.get_tag(new_location, skip_sync=True)
                    location = new_location
                except Tag.DoesNotExist:
                    # Not a group, remove the second argument from the link
                    extra = text[text.find(second):]
                    text = text[:text.find(second)]

            link = reverse("content:tag", kwargs={"location": location})
            return f"[{text}]({link}){extra}"
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
