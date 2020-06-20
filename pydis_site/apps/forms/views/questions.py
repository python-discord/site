import json

from django.contrib.messages import ERROR, add_message
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from pydis_site.apps.forms.models import Form


class FormQuestionsView(View):
    """Routes for updating the questions on a form."""

    def post(self, request: HttpRequest, form_id: str) -> HttpResponse:
        """Save the question data to the form."""
        if not request.user.has_perm("forms.change_form"):
            add_message(request, ERROR, "You do not have permission to access this page.")
            return redirect(reverse("home"))

        form = get_object_or_404(Form, id=form_id)

        questions = json.loads(request.body)["questions"]

        if len(set([q["id"] for q in questions])) != len(questions):
            return JsonResponse({
                "status": "error",
                "message": "Two questions have the same ID"
            })

        form.questions = questions
        form.save()

        return JsonResponse({
            "status": "success"
        })
