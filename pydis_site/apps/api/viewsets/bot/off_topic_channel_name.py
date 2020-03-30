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
    ... then the API will return `5` random items from the database.
    If the `mark_used` query parameter is given like...
        $ curl api.pydis.local:8000/bot/off-topic-channel-names?random_items=5&mark_used=true
    ... then the API will mark returned `5` items `used`.
    When running out of names, API will mark all names to not used and start new round.

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

            if 'mark_used' in request.query_params and request.query_params['mark_used']:
                queryset = self.get_queryset().order_by('?').exclude(used=True)[:random_count]
                self.get_queryset().filter(
                    name__in=(query.name for query in queryset)
                ).update(used=True)

                # When client request more channel names than non-used names is available, start
                # new round of names.
                if len(queryset) < random_count:
                    # Get how much names still missing and don't fetch duplicate names.
                    need_more = random_count - len(queryset)
                    ext = self.get_queryset().order_by('?').exclude(
                        name__in=(query.name for query in queryset)
                    )[:need_more]

                    # Set all names `used` field to False except these that we just used.
                    self.get_queryset().exclude(name__in=(
                        query.name for query in ext)
                    ).update(used=False)
                    # Join original queryset (that had missing names)
                    # and extension with these missing names.
                    queryset = list(queryset) + list(ext)
                serialized = self.serializer_class(queryset, many=True)
                return Response(serialized.data)

            queryset = self.get_queryset().order_by('?')[:random_count]
            serialized = self.serializer_class(queryset, many=True)
            return Response(serialized.data)

        queryset = self.get_queryset()
        serialized = self.serializer_class(queryset, many=True)
        return Response(serialized.data)
