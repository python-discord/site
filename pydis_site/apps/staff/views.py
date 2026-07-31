from django.db.models import Prefetch
from django.views.generic.detail import DetailView

from pydis_site.apps.api.models.bot.deleted_message import DeletedMessage
from pydis_site.apps.api.models.bot.message_deletion_context import MessageDeletionContext


class LogView(DetailView):
    """The default view for the Deleted Messages logs."""

    model = MessageDeletionContext
    context_object_name = "deletion_context"
    template_name = "staff/logs.html"
    queryset = MessageDeletionContext.objects.select_related("actor").prefetch_related(
        Prefetch(
            "deletedmessage_set",
            queryset=DeletedMessage.objects.select_related("author"),
        ),
    )
