from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot.scheduled_event import ScheduledEvent
from pydis_site.apps.api.serializers import ScheduledEventSerializer


class ScheduledEventViewSet(ModelViewSet):
    """TODO: DOCS."""

    queryset = ScheduledEvent.objects.select_related("user_event").all()
    serializer_class = ScheduledEventSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ("user_event__organizer", "user_event__name")
