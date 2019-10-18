from django.contrib import messages
from django.http import HttpRequest
from django.views.generic import RedirectView


class MessageRedirectView(RedirectView):
    """
    Redirects to another URL, also setting a message using the Django Messages framework.

    This is based on Django's own `RedirectView` and works the same way, but takes two additional
    parameters.

    * `message`: Set to the message content you wish to display.
    * `message_level`: Set to one of the message levels from the Django messages framework. This
        parameter defaults to `messages.INFO`.
    """

    message: str = ""
    message_level: int = messages.INFO

    def get(self, request: HttpRequest, *args, **kwargs) -> None:
        """Called upon a GET request."""
        messages.add_message(request, self.message_level, self.message)

        return super().get(request, *args, **kwargs)
