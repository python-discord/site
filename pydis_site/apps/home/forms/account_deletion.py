from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django.forms import CharField, Form
from django_crispy_bulma.layout import IconField, Submit


class AccountDeletionForm(Form):
    """Account deletion form, to collect username for confirmation of removal."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "I understand, delete my account"))

        self.helper.layout = Layout(
            IconField("username", icon_prepend="user")
        )

    username = CharField(
        label="Username",
        required=True
    )
