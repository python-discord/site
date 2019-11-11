from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers import registry
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import ERROR, INFO, add_message
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View


class SettingsView(LoginRequiredMixin, View):
    """
    Account settings view, for managing and deleting user accounts and connections.

    This view actually renders a template with a bare modal, and is intended to be
    inserted into another template using JavaScript.
    """

    def __init__(self, *args, **kwargs):
        self.login_url = reverse("home")
        super().__init__(*args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        """HTTP GET: Return the view template."""
        context = {
            "groups": request.user.groups.all(),

            "discord": None,
            "github": None,

            "discord_provider": registry.provider_map.get("discord"),
            "github_provider": registry.provider_map.get("github"),
        }

        for account in SocialAccount.objects.filter(user=request.user).all():
            if account.provider == "discord":
                context["discord"] = account

            if account.provider == "github":
                context["github"] = account

        return render(request, "home/account/settings.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """HTTP POST: Process account disconnections."""
        provider = request.POST["provider"]

        if provider == "github":
            try:
                account = SocialAccount.objects.get(user=request.user, provider=provider)
            except SocialAccount.DoesNotExist:
                add_message(request, ERROR, "You do not have a GitHub account linked.")
            else:
                account.delete()
                add_message(request, INFO, "The social account has been disconnected.")
        else:
            add_message(request, ERROR, f"Unknown provider: {provider}")

        return redirect(reverse("home"))
