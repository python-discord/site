from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import ERROR, INFO, add_message
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from pydis_site.apps.home.forms.account_deletion import AccountDeletionForm


class DeleteView(LoginRequiredMixin, View):
    """Account deletion view, for removing linked user accounts from the DB."""

    def __init__(self, *args, **kwargs):
        self.login_url = reverse("home")
        super().__init__(*args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        """HTTP GET: Return the view template."""
        return render(
            request, "home/account/delete.html",
            context={"form": AccountDeletionForm()}
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        """HTTP POST: Process the deletion, as requested by the user."""
        form = AccountDeletionForm(request.POST)

        if not form.is_valid() or request.user.username != form.cleaned_data["username"]:
            add_message(request, ERROR, "Please enter your username exactly as shown.")

            return redirect(reverse("account_delete"))

        request.user.delete()
        add_message(request, INFO, "Your account has been deleted.")

        return redirect(reverse("home"))
