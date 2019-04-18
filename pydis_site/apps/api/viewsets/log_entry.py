from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.log_entry import LogEntry
from pydis_site.apps.api.serializers import LogEntrySerializer


class LogEntryViewSet(CreateModelMixin, GenericViewSet):
    """
    View providing support for creating log entries in the site database
    for viewing via the log browser.

    ## Routes
    ### POST /logs
    Create a new log entry.

    #### Request body
    >>> {
    ...     'application': str,  # 'bot' | 'seasonalbot' | 'site'
    ...     'logger_name': str,  # such as 'bot.cogs.moderation'
    ...     'timestamp': Optional[str],  # from `datetime.utcnow().isoformat()`
    ...     'level': str,  # 'debug' | 'info' | 'warning' | 'error' | 'critical'
    ...     'module': str,  # such as 'pydis_site.apps.api.serializers'
    ...     'line': int,  # > 0
    ...     'message': str,  # textual formatted content of the logline
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if the request body has invalid fields, see the response for details

    ## Authentication
    Requires a API token.
    """

    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
