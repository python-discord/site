from django.forms import CharField, Form


class AccountDeletionForm(Form):
    """Account deletion form, to collect username for confirmation of removal."""

    username = CharField(
        label="Username",
        required=True
    )
