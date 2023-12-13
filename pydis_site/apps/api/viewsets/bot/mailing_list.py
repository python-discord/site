from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.serializers import MailingListSerializer
from pydis_site.apps.api.models import MailingList, MailingListSeenItem


class MailingListViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin):
    """
    View providing management and updates of mailing lists and their seen items.

    ## Routes

    ### GET /bot/mailing-lists
    Returns all the mailing lists and their seen items.

    #### Response format
    >>> [
    ...     {
    ...         'id': 1,
    ...         'name': 'python-dev',
    ...         'seen_items': [
    ...             'd81gg90290la8',
    ...             ...
    ...         ]
    ...     },
    ...     ...
    ... ]

    ### POST /bot/mailing-lists
    Create a new mailing list.

    #### Request format
    >>> {
    ...     'name': str
    ... }

    #### Status codes
    - 201: when the mailing list was created successfully
    - 400: if the request data was invalid

    ### GET /bot/mailing-lists/<name:str>
    Retrieve a single mailing list and its seen items.

    #### Response format
    >>> {
    ...     'id': 1,
    ...     'name': 'python-dev',
    ...     'seen_items': [
    ...         'd81gg90290la8',
    ...         ...
    ...     ]
    ... }

    ### POST /bot/mailing-lists/<name:str>/seen-items
    Add a single seen item to the given mailing list. The request body should
    be the hash of the seen item to add, as a plain string.

    #### Request body
    >>> str

    #### Response format
    Empty response.

    #### Status codes
    - 204: on successful creation of the seen item
    - 400: if the request data was invalid
    - 404: when the mailing list with the given name could not be found
    """

    lookup_field = 'name'
    serializer_class = MailingListSerializer
    queryset = MailingList.objects.prefetch_related('seen_items')

    @action(detail=True, methods=["POST"],
            name="Add a seen item for a mailing list", url_name='seen-items', url_path='seen-items')
    def add_seen_item(self, request: Request, name: str) -> Response:
        """Add a single seen item to the given mailing list."""
        if not isinstance(request.data, str):
            raise ParseError(detail={'non_field_errors': ["The request body must be a string"]})

        list_ = self.get_object()
        seen_item = MailingListSeenItem(list=list_, hash=request.data)
        try:
            seen_item.save()
        except IntegrityError as err:
            if err.__cause__.diag.constraint_name == 'unique_list_and_hash':
                raise ParseError(detail={'non_field_errors': ["Seen item already known."]})
            raise  # pragma: no cover

        return Response(status=status.HTTP_204_NO_CONTENT)
