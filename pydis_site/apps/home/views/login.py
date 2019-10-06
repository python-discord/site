from allauth.socialaccount.providers import registry
from allauth.socialaccount.providers.discord.provider import DiscordProvider
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin


class LoginView(View, TemplateResponseMixin):
    """Login view for collecting email collection consent from users."""

    template_name = "home/login.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render the login page view."""
        return self.render_to_response({})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Check whether the user provided consent, and action appropriately."""
        if request.POST.get("consent", None) != "on":  # I bet IE breaks this standard...
            messages.add_message(
                request,
                messages.ERROR,
                "Consent is required to login with Discord.",
            )

            return self.render_to_response({})

        provider: DiscordProvider = registry.by_id("discord")
        return redirect(provider.get_login_url(request))
