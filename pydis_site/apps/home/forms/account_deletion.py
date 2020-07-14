from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django.forms import CharField, Form


class AccountDeletionForm(Form):
    """Account deletion form, to collect username for confirmation of removal."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "I understand, delete my account", css_class='button is-primary'))

        self.helper.layout = Layout(
            Field("username")
        )

    username = CharField(
        label="Username",
        required=True
    )
