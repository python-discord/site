from django.db.models import Case, Value, When
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ViewSet

from pydis_site.apps.api.models.bot.off_topic_channel_name import OffTopicChannelName
from pydis_site.apps.api.serializers import OffTopicChannelNameSerializer


class OffTopicChannelNameViewSet(DestroyModelMixin, ViewSet):
    """
    View of off-topic channel names used by the bot to rotate our off-topic names on a daily basis.

    ## Routes
    ### GET /bot/off-topic-channel-names
    Return all known off-topic channel names from the database.
    If the `random_items` query parameter is given, for example using...
        $ curl api.pythondiscord.local:8000/bot/off-topic-channel-names?random_items=5
    ... then the API will return `5` random items from the database
    that is not used in current rotation.
    When running out of names, API will mark all names to not used and start new rotation.

    #### Response format
    Return a list of off-topic-channel names:
    >>> [
    ...     "lemons-lemonade-stand",
    ...     "bbq-with-bisk"
    ... ]

    #### Status codes
    - 200: returned on success
    - 400: returned when `random_items` is not a positive integer

    ### POST /bot/off-topic-channel-names
    Create a new off-topic-channel name in the database.
    The name must be given as a query parameter, for example:
        $ curl api.pythondiscord.local:8000/bot/off-topic-channel-names?name=lemons-lemonade-shop

    #### Status codes
    - 201: returned on success
    - 400: if the request body has invalid fields, see the response for details

    ### DELETE /bot/off-topic-channel-names/<name:str>
    Delete the off-topic-channel name with the given `name`.

    #### Status codes
    - 204: returned on success
    - 404: returned when the given `name` was not found

    ## Authentication
    Requires a API token.
    """

    lookup_field = 'name'
    serializer_class = OffTopicChannelNameSerializer

    def get_object(self) -> OffTopicChannelName:
        """
        Returns the OffTopicChannelName entry for this request, if it exists.

        If it doesn't, a HTTP 404 is returned by way of throwing an exception.
        """
        queryset = self.get_queryset()
        name = self.kwargs[self.lookup_field]
        return get_object_or_404(queryset, name=name)

    def get_queryset(self) -> QuerySet:
        """Returns a queryset that covers the entire OffTopicChannelName table."""
        return OffTopicChannelName.objects.all()

    def create(self, request: HttpRequest) -> Response:
        """
        DRF method for creating a new OffTopicChannelName.

        Called by the Django Rest Framework in response to the corresponding HTTP request.
        """
        if 'name' in request.query_params:
            create_data = {'name': request.query_params['name']}
            serializer = OffTopicChannelNameSerializer(data=create_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(create_data, status=HTTP_201_CREATED)

        else:
            raise ParseError(detail={
                'name': ["This query parameter is required."]
            })

    def list(self, request: HttpRequest) -> Response:
        """
        DRF method for listing OffTopicChannelName entries.

        Called by the Django Rest Framework in response to the corresponding HTTP request.
        """
        if 'random_items' in request.query_params:
            param = request.query_params['random_items']
            try:
                random_count = int(param)
            except ValueError:
                raise ParseError(detail={'random_items': ["Must be a valid integer."]})

            if random_count <= 0:
                raise ParseError(detail={
                    'random_items': ["Must be a positive integer."]
                })

            queryset = self.get_queryset().order_by('used', '?')[:random_count]

            # When any name is used in our listing then this means we reached end of round
            # and we need to reset all other names `used` to False
            if any(offtopic_name.used for offtopic_name in queryset):
                # These names that we just got have to be excluded from updating used to False
                self.get_queryset().update(
                    used=Case(
                        When(
                            name__in=(offtopic_name.name for offtopic_name in queryset),
                            then=Value(True)
                        ),
                        default=Value(False)
                    )
                )
            else:
                # Otherwise mark selected names `used` to True
                self.get_queryset().filter(
                    name__in=(offtopic_name.name for offtopic_name in queryset)
                ).update(used=True)

            serialized = self.serializer_class(queryset, many=True)
            return Response(serialized.data)

        queryset = self.get_queryset()
        serialized = self.serializer_class(queryset, many=True)
        return Response(serialized.data)
