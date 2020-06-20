from django.contrib.postgres.fields import JSONField
from django.db import models


class Form(models.Model):
    """Model representing a survey/form."""

    id = models.CharField(
        unique=True,
        max_length=60,
        help_text="The unique ID used in the sharing link for the form",
        primary_key=True
    )
    title = models.TextField(help_text="The title of the form as displayed in the header section")
    public = models.BooleanField(
        default=False,
        help_text="Whether this form should be publicly accessible"
    )

    needs_oauth = models.BooleanField(
        default=False,
        help_text="Collect OAuth2 data from users filling out the form"
    )

    # Questions should not be editable since it is too complex ffor the Django Admin UI
    # Instead we set editable to false and we edit forms through the form management portal
    questions = JSONField(
        help_text="The questions on the form in JSON format",
        editable=False,
        default=dict
    )
