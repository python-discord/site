from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from pydis_site.apps.api.models.bot.message_deletion_context import MessageDeletionContext


class LogView(View):
    template_name = "staff/logs.html"

    def get(self, request: WSGIRequest, pk: int) -> HttpResponse:
        message_context = get_object_or_404(MessageDeletionContext, pk=pk)
        messages = message_context.deletedmessage_set.all()
        return render(request, self.template_name, {"message_context": message_context, "messages": messages})
