from django.apps import AppConfig


class HomeConfig(AppConfig):
    """Django AppConfig for the home app."""

    name = 'pydis_site.apps.home'
    signal_listener = None

    def ready(self) -> None:
        """Run when the app has been loaded and is ready to serve requests."""
        from pydis_site.apps.home.signals import SignalListener

        self.signal_listener = SignalListener()
