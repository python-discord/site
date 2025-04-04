import platform

from django.conf import settings
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response

from .authentication import JWTAuthentication


class IndexView(APIView):
    """
    Return a generic hello world message with some information to the client.

    Can be used as a healthcheck for Kubernetes or a frontend connection check.

    ## Response format

    The response is a JSON map with the following fields:

    - `message` (`str`): A hello message.
    - `client` (`str`): IP address of the connecting client. This might be an
      internal load balancer IP.
    - `sha` (`str`): Git hash of the current release.
    - `node` (`str`): Hostname of the node that processed the request.
    - `user`? (`dict`): Carries information about the requesting client. Only
      present when the client is authenticated. The following keys are
      included:
      - `authenticated` (`bool`): Always `True`.
      - `user` (`dict`): All user information stored in the requesting JWT
        token.
      - `scopes` (`list[str]`): A list of JWT scopes the user is authenticated
        with.
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = ()

    def get(self, request: HttpRequest, format: str | None = None) -> Response:
        """Return a hello from Python Discord forms!"""
        response_data = {
            "message": "Hello, world!",
            "client": request.META["REMOTE_ADDR"],
            "user": {
                "authenticated": False,
            },
            "sha": settings.GIT_SHA,
            "node": platform.uname().node,
        }

        if request.user.is_authenticated:
            response_data["user"] = {
                "authenticated": True,
                "user": request.user.payload,
                "scopes": request.auth.scopes,
            }

        return Response(response_data)
