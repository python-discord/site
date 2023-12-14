from django.views.generic.detail import DetailView

from pydis_site.apps.api.models.bot.message_deletion_context import MessageDeletionContext


class LogView(DetailView):
    """The default view for the Deleted Messages logs."""

    model = MessageDeletionContext
    context_object_name = "deletion_context"
    template_name = "staff/logs.html"
