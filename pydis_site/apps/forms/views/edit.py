from django.contrib.messages import ERROR, add_message
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from pydis_site.apps.forms.models import Form


class FormEditView(View):
    """Return a view for editing a specific form."""

    def get(self, request: HttpRequest, form_id: str) -> HttpResponse:
        """Return the form editing page for given form_id."""
        if not request.user.has_perm("forms.change_form"):
            add_message(request, ERROR, "You do not have permission to access this page.")
            return redirect(reverse("home"))

        form = get_object_or_404(Form, id=form_id)

        return render(request, "forms/edit.html", {"form": form})

    def post(self, request: HttpRequest, form_id: str) -> HttpResponse:
        """Update a form with the given parameters."""
        if not request.user.has_perm("forms.change_form"):
            add_message(request, ERROR, "You do not have permission to access this page.")
            return redirect(reverse("home"))

        form = get_object_or_404(Form, id=form_id)

        form.public = request.POST.get("public") == "on"
        form.needs_oauth = request.POST.get("needs_oauth") == "on"

        form.save()

        return render(request, "forms/edit.html", {"form": form})