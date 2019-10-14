from typing import Any, Dict

from django.apps import AppConfig


class HomeConfig(AppConfig):
    """Django AppConfig for the home app."""

    name = 'pydis_site.apps.home'
    signal_listener = None

    def ready(self) -> None:
        """Run when the app has been loaded and is ready to serve requests."""
        from pydis_site.apps.home.signals import AllauthSignalListener

        self.signal_listener = AllauthSignalListener()
        self.patch_allauth()

    def patch_allauth(self) -> None:
        """Monkey-patches Allauth classes so we never collect email addresses."""
        # Imported here because we can't import it before our apps are loaded up
        from allauth.socialaccount.providers.base import Provider

        def extract_extra_data(_: Provider, data: Dict[str, Any]) -> Dict[str, Any]:
            """
            Extracts extra data for a SocialAccount provided by Allauth.

            This is our version of this function that strips the email address from incoming extra
            data. We do this so that we never have to store it.

            This is monkey-patched because most OAuth providers - or at least the ones we care
            about - all use the function from the base Provider class. This means we don't have
            to make a new Django app for each one we want to work with.
            """
            data["email"] = ""
            return data

        Provider.extract_extra_data = extract_extra_data
