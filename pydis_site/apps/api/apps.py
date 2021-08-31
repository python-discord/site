from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Django AppConfig for the API app."""

    name = 'pydis_site.apps.api'

    def ready(self) -> None:
        """
        Gets called as soon as the registry is fully populated.

        https://docs.djangoproject.com/en/3.2/ref/applications/#django.apps.AppConfig.ready
        """
        import pydis_site.apps.api.signals  # noqa: F401
