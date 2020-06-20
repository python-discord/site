from django.contrib.messages import ERROR, add_message
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from pydis_site.apps.forms.models import Form


class FormIndexView(View):
    """Return the form management page."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Return the form management page if the user is authorized to view this."""
        if not request.user.has_perm("forms.change_form"):
            add_message(request, ERROR, "You do not have permission to access this page.")
            return redirect(reverse("home"))

        forms = Form.objects.all()

        return render(request, "forms/index.html", {"forms": forms})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Create a new form with provided title and ID."""
        if not request.user.has_perm("forms.change_form"):
            add_message(request, ERROR, "You do not have permission to access this page.")
            return redirect(reverse("home"))

        form = Form(id=request.POST["id"], title=request.POST["title"])

        form.save()

        return redirect(reverse("forms:edit_form", kwargs={"form_id": form.id}))
