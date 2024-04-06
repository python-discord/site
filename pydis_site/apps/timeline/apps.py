from pathlib import Path

from django.apps import AppConfig
import frontmatter
import markdown

from pydis_site import settings


ENTRIES_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "timeline", "entries")


class TimelineConfig(AppConfig):
    """AppConfig instance for Timeline app."""

    name = 'pydis_site.apps.timeline'

    def ready(self) -> None:
        """Fetch all the timeline entries."""
        self.entries = []

        for path in ENTRIES_PATH.rglob("*.md"):
            metadata, content = frontmatter.parse(path.read_text(encoding="utf-8"))

            md = markdown.Markdown()
            html = str(md.convert(content))

            # Strip `.md` file extension from filename and split it into the
            # date (for sorting) and slug (for linking).
            key, slug = path.name[:-3].split("_")

            icon_color = metadata.get("icon_color")
            # Use the pydis blurple as the default background color.
            if not icon_color or metadata["icon"] == "pydis":
                icon_color = "has-background-primary"

            entry = {
                "key": key,
                "slug": slug,
                "title": metadata["title"],
                "date": metadata["date"],
                "icon": metadata["icon"],
                "icon_color": icon_color,
                "content": html,
            }

            self.entries.append(entry)

        # Sort the entries in reverse-chronological order.
        self.entries.sort(key=lambda e: e['key'], reverse=True)
