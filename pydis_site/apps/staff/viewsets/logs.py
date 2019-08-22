import logging

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from pydis_site.apps.api.models.bot.message_deletion_context import MessageDeletionContext

log = logging.getLogger(__name__)


class LogView(View):
    """The default view for the Deleted Messages logs."""

    template_name = "staff/logs.html"

    def get(self, request: WSGIRequest, pk: int) -> HttpResponse:
        """Get method that answers a request with an html response by rendering a template."""
        message_context = get_object_or_404(MessageDeletionContext, pk=pk)

        actor = message_context.actor
        creation = message_context.creation
        messages = message_context.deletedmessage_set.all()

        template_fields = {
            'actor': actor,
            'actor_colour': message_context.actor.top_role.colour,
            'creation': creation,
            'messages': messages
        }

        return render(request, self.template_name, template_fields)
