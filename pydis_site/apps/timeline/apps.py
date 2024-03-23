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
            entry = {
                "key": key,
                "slug": slug,
                "title": metadata["title"],
                "date": metadata["date"],
                "icon": metadata["icon"],
                # This key might not be used if the icon uses the pydis logo.
                "icon_color": metadata.get("icon_color"),
                "content": html,
            }

            self.entries.append(entry)

        # Sort the entries in reverse-chronological order.
        self.entries.sort(key=lambda e: e['key'], reverse=True)
