from rest_framework.response import Response
from rest_framework.views import APIView


class HealthcheckView(APIView):
    """
    Provides a simple view to check that the website is alive and well.

    ## Routes
    ### GET /healthcheck
    Returns a simple JSON document showcasing whether the system is working:

    >>> {
    ...     'status': 'ok'
    ... }

    Seems to be.

    ## Authentication
    Does not require any authentication nor permissions..
    """

    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        return Response({'status': 'ok'})
