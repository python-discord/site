from pathlib import Path

from django.apps import AppConfig

from pydis_site import settings

RESOURCES_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "resources", "resources")


class ResourcesConfig(AppConfig):
    """AppConfig instance for Resources app."""

    name = 'pydis_site.apps.resources'
