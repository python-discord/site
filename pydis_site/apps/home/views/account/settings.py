from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View


class SettingsView(LoginRequiredMixin, View):
    """Account settings view, for managing and deleting user accounts and connections."""

    def __init__(self, *args, **kwargs):
        self.login_url = reverse("home")
        super().__init__(*args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        """HTTP GET: Return the view template."""
        return render(request, "home/account/settings.html")
