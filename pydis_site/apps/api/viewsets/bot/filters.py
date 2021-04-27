from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot.filters import (  # noqa: I101 - Preserving the filter order
    FilterList,
    FilterSettings,
    FilterAction,
    ChannelRange,
    Filter,
    FilterOverride
)
from pydis_site.apps.api.serializers import (  # noqa: I101 - Preserving the filter order
    FilterListSerializer,
    FilterSettingsSerializer,
    FilterActionSerializer,
    FilterChannelRangeSerializer,
    FilterSerializer,
    FilterOverrideSerializer
)


class FilterListViewSet(ModelViewSet):
    """
    View providing CRUD operations on lists of items allowed or denied by our bot.

    ## Routes
    ### GET /bot/filter/filter_lists
    Returns all FilterList items in the database.

    #### Response format
    >>> [
    ...     {
    ...         "id": 1,
    ...         "name": "guild_invite",
    ...         "list_type": 1,
    ...         "filters": [
    ...             1,
    ...             2,
    ...             ...
    ...         ],
    ...         "default_settings": 1
    ...     },
    ...     ...
    ... ]

    #### Status codes
    - 200: returned on success
    - 401: returned if unauthenticated

    ### GET /bot/filter/filter_lists/<id:int>
    Returns a specific FilterList item from the database.

    #### Response format
    >>> {
    ...     "id": 1,
    ...     "name": "guild_invite",
    ...     "list_type": 1,
    ...     "filters": [
    ...         1,
    ...         2,
    ...         ...
    ...     ],
    ...     "default_settings": 1
    ... }

    #### Status codes
    - 200: returned on success
    - 404: returned if the id was not found.

    ### POST /bot/filter/filter_lists
    Adds a single FilterList item to the database.

    #### Request body
    >>> {
    ...     "name": "guild_invite",
    ...     "list_type": 1,
    ...     "filters": [
    ...         1,
    ...         2,
    ...         ...
    ...     ],
    ...     "default_settings": 1
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if one of the given fields is invalid

    ### PATCH /bot/filter/filter_lists/<id:int>
    Updates a specific FilterList item from the database.

    #### Response format
    >>> {
    ...     "id": 1,
    ...     "name": "guild_invite",
    ...     "list_type": 1,
    ...     "filters": [
    ...         1,
    ...         2,
    ...         ...
    ...     ],
    ...     "default_settings": 1
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if one of the given fields is invalid

    ### DELETE /bot/filter/filter_lists/<id:int>
    Deletes the FilterList item with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a tag with the given `id` does not exist
    """

    serializer_class = FilterListSerializer
    queryset = FilterList.objects.all()


class FilterSettingsViewSet(ModelViewSet):
    """
    View providing CRUD operations on settings of items allowed or denied by our bot.

    ## Routes
    ### GET /bot/filter/filter_settings
    Returns all FilterSettings items in the database.

    #### Response format
    >>> [
    ...     {
    ...         "id": 1,
    ...         "ping_type": [
    ...             "onduty",
    ...              ...
    ...          ],
    ...         "filter_dm": True,
    ...         "dm_ping_type": [
    ...             "onduty",
    ...             ...
    ...         ],
    ...         "delete_messages": True,
    ...         "bypass_roles": [
    ...             267630620367257601,
    ...             ...
    ...         ],
    ...         "enabled": True,
    ...         "default_action": 1,
    ...         "default_range": 1
    ...     },
    ...     ...
    ... ]

    #### Status codes
    - 200: returned on success
    - 401: returned if unauthenticated

    ### GET /bot/filter/filter_settings/<id:int>
    Returns a specific FilterSettings item from the database.

    #### Response format
    >>> {
    ...     "id": 1,
    ...     "ping_type": [
    ...         "onduty",
    ...          ...
    ...     ],
    ...     "filter_dm": True,
    ...     "dm_ping_type": [
    ...         "onduty",
    ...         ...
    ...     ],
    ...     "delete_messages": True,
    ...     "bypass_roles": [
    ...         267630620367257601,
    ...         ...
    ...     ],
    ...     "enabled": True,
    ...     "default_action": 1,
    ...     "default_range": 1
    ... }

    #### Status codes
    - 200: returned on success
    - 404: returned if the id was not found.

    ### POST /bot/filter/filter_settings
    Adds a single FilterSettings item to the database.

    #### Request body
    >>> {
    ...     "ping_type": [
    ...         "onduty",
    ...          ...
    ...     ],
    ...     "filter_dm": True,
    ...     "dm_ping_type": [
    ...         "onduty",
    ...         ...
    ...     ],
    ...     "delete_messages": True,
    ...     "bypass_roles": [
    ...         267630620367257601,
    ...         ...
    ...     ],
    ...     "enabled": True,
    ...     "default_action": 1,
    ...     "default_range": 1
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if one of the given fields is invalid

    ### PATCH /bot/filter/filter_settings/<id:int>
    Updates a specific FilterSettings item from the database.

    #### Response format
    >>> {
    ...     "id": 1,
    ...     "ping_type": [
    ...         "onduty",
    ...          ...
    ...     ],
    ...     "filter_dm": True,
    ...     "dm_ping_type": [
    ...         "onduty",
    ...         ...
    ...     ],
    ...     "delete_messages": True,
    ...     "bypass_roles": [
    ...         267630620367257601,
    ...         ...
    ...     ],
    ...     "enabled": True,
    ...     "default_action": 1,
    ...     "default_range": 1
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if one of the given fields is invalid

    ### DELETE /bot/filter/filter_settings/<id:int>
    Deletes the FilterSettings item with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a tag with the given `id` does not exist
    """

    serializer_class = FilterSettingsSerializer
    queryset = FilterSettings.objects.all()


class FilterActionViewSet(ModelViewSet):
    """
    View providing CRUD operations on actions taken by items allowed or denied by our bot.

    ## Routes
    ### GET /bot/filter/filter_action
    Returns all FilterAction items in the database.

    #### Response format
    >>> [
    ...     {
    ...         "id": 1,
    ...         "user_dm": "message",
    ...         "infraction_type": "Warn",
    ...         "infraction_reason": "",
    ...         "infraction_duration": "01 12:34:56.123456"
    ...     },
    ...     ...
    ... ]

    #### Status codes
    - 200: returned on success
    - 401: returned if unauthenticated

    ### GET /bot/filter/filter_action/<id:int>
    Returns a specific FilterAction item from the database.

    #### Response format
    >>> {
    ...     "id": 1,
    ...     "user_dm": "message",
    ...     "infraction_type": "Warn",
    ...     "infraction_reason": "",
    ...     "infraction_duration": "01 12:34:56.123456"
    ... }

    #### Status codes
    - 200: returned on success
    - 404: returned if the id was not found.

    ### POST /bot/filter/filter_action
    Adds a single FilterAction item to the database.

    #### Request body
    >>> {
    ...     "user_dm": "message",
    ...     "infraction_type": "Warn",
    ...     "infraction_reason": "",
    ...     "infraction_duration": "01 12:34:56.123456"
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if one of the given fields is invalid

    ### PATCH /bot/filter/filter_action/<id:int>
    Updates a specific FilterAction item from the database.

    #### Response format
    >>> {
    ...     "id": 1,
    ...     "user_dm": "message",
    ...     "infraction_type": "Warn",
    ...     "infraction_reason": "",
    ...     "infraction_duration": "01 12:34:56.123456"
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if one of the given fields is invalid

    ### DELETE /bot/filter/filter_action/<id:int>
    Deletes the FilterAction item with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a tag with the given `id` does not exist
    """

    serializer_class = FilterActionSerializer
    queryset = FilterAction.objects.all()


class FilterChannelRangeViewSet(ModelViewSet):
    """
    View providing CRUD operations on channels targeted by items allowed or denied by our bot.

    ## Routes
    ### GET /bot/filter/channel_range
    Returns all ChannelRange items in the database.

    #### Response format
    >>> [
    ...     {
    ...         "id": 1,
    ...         "disallowed_channels": [],
    ...         "disallowed_categories": [],
    ...         "allowed_channels": [],
    ...         "allowed_category": [],
    ...         "default": True
    ...     },
    ...     ...
    ... ]

    #### Status codes
    - 200: returned on success
    - 401: returned if unauthenticated

    ### GET /bot/filter/channel_range/<id:int>
    Returns a specific ChannelRange item from the database.

    #### Response format
    >>> {
    ...     "id": 1,
    ...     "disallowed_channels": [],
    ...     "disallowed_categories": [],
    ...     "allowed_channels": [],
    ...     "allowed_category": [],
    ...     "default": True
    ... }

    #### Status codes
    - 200: returned on success
    - 404: returned if the id was not found.

    ### POST /bot/filter/channel_range
    Adds a single ChannelRange item to the database.

    #### Request body
    >>> {
    ...     "disallowed_channels": [],
    ...     "disallowed_categories": [],
    ...     "allowed_channels": [],
    ...     "allowed_category": [],
    ...     "default": True
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if one of the given fields is invalid

    ### PATCH /bot/filter/channel_range/<id:int>
    Updates a specific ChannelRange item from the database.

    #### Response format
    >>> {
    ...     "id": 1,
    ...     "disallowed_channels": [],
    ...     "disallowed_categories": [],
    ...     "allowed_channels": [],
    ...     "allowed_category": [],
    ...     "default": True
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if one of the given fields is invalid

    ### DELETE /bot/filter/channel_range/<id:int>
    Deletes the ChannelRange item with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a tag with the given `id` does not exist
    """

    serializer_class = FilterChannelRangeSerializer
    queryset = ChannelRange.objects.all()


class FilterViewSet(ModelViewSet):
    """
    View providing CRUD operations on items allowed or denied by our bot.

    ## Routes
    ### GET /bot/filter/filters
    Returns all Filter items in the database.

    #### Response format
    >>> [
    ...     {
    ...         "id": 1,
    ...         "content": "267624335836053506",
    ...         "description": "Python Discord",
    ...         "additional_field": None,
    ...         "override": 1
    ...     },
    ...     ...
    ... ]

    #### Status codes
    - 200: returned on success
    - 401: returned if unauthenticated

    ### GET /bot/filter/filters/<id:int>
    Returns a specific Filter item from the database.

    #### Response format
    >>> {
    ...     "id": 1,
    ...     "content": "267624335836053506",
    ...     "description": "Python Discord",
    ...     "additional_field": None,
    ...     "override": 1
    ... }

    #### Status codes
    - 200: returned on success
    - 404: returned if the id was not found.

    ### POST /bot/filter/filters
    Adds a single Filter item to the database.

    #### Request body
    >>> {
    ...     "content": "267624335836053506",
    ...     "description": "Python Discord",
    ...     "additional_field": None,
    ...     "override": 1
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if one of the given fields is invalid

    ### PATCH /bot/filter/filters/<id:int>
    Updates a specific Filter item from the database.

    #### Response format
    >>> {
    ...     "id": 1,
    ...     "content": "267624335836053506",
    ...     "description": "Python Discord",
    ...     "additional_field": None,
    ...     "override": 1
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if one of the given fields is invalid

    ### DELETE /bot/filter/filters/<id:int>
    Deletes the Filter item with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a tag with the given `id` does not exist
    """

    serializer_class = FilterSerializer
    queryset = Filter.objects.all()


class FilterOverrideViewSet(ModelViewSet):
    """
    View providing CRUD operations setting overrides of items allowed or denied by our bot.

    ## Routes
    ### GET /bot/filter/filter_override
    Returns all FilterOverride items in the database.

    #### Response format
    >>> [
    ...     {
    ...         "id": 1,
    ...         "ping_type": [
    ...             "onduty",
    ...              ...
    ...          ],
    ...         "filter_dm": True,
    ...         "dm_ping_type": [
    ...             "onduty",
    ...             ...
    ...         ],
    ...         "delete_messages": True,
    ...         "bypass_roles": [
    ...             267630620367257601,
    ...             ...
    ...         ],
    ...         "enabled": True,
    ...         "filter_action": 1,
    ...         "filter_range": 1
    ...     },
    ...     ...
    ... ]

    #### Status codes
    - 200: returned on success
    - 401: returned if unauthenticated

    ### GET /bot/filter/filter_override/<id:int>
    Returns a specific FilterOverride item from the database.

    #### Response format
    >>> {
    ...     "id": 1,
    ...     "ping_type": [
    ...         "onduty",
    ...          ...
    ...     ],
    ...     "filter_dm": True,
    ...     "dm_ping_type": [
    ...         "onduty",
    ...         ...
    ...     ],
    ...     "delete_messages": True,
    ...     "bypass_roles": [
    ...         267630620367257601,
    ...         ...
    ...     ],
    ...     "enabled": True,
    ...     "filter_action": 1,
    ...     "filter_range": 1
    ... }

    #### Status codes
    - 200: returned on success
    - 404: returned if the id was not found.

    ### POST /bot/filter/filter_override
    Adds a single FilterOverride item to the database.

    #### Request body
    >>> {
    ...     "ping_type": [
    ...         "onduty",
    ...          ...
    ...     ],
    ...     "filter_dm": True,
    ...     "dm_ping_type": [
    ...         "onduty",
    ...         ...
    ...     ],
    ...     "delete_messages": True,
    ...     "bypass_roles": [
    ...         267630620367257601,
    ...         ...
    ...     ],
    ...     "enabled": True,
    ...     "filter_action": 1,
    ...     "filter_range": 1
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if one of the given fields is invalid

    ### PATCH /bot/filter/filter_override/<id:int>
    Updates a specific FilterOverride item from the database.

    #### Response format
    >>> {
    ...     "id": 1,
    ...     "ping_type": [
    ...         "onduty",
    ...          ...
    ...     ],
    ...     "filter_dm": True,
    ...     "dm_ping_type": [
    ...         "onduty",
    ...         ...
    ...     ],
    ...     "delete_messages": True,
    ...     "bypass_roles": [
    ...         267630620367257601,
    ...         ...
    ...     ],
    ...     "enabled": True,
    ...     "filter_action": 1,
    ...     "filter_range": 1
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if one of the given fields is invalid

    ### DELETE /bot/filter/filter_override/<id:int>
    Deletes the FilterOverride item with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a tag with the given `id` does not exist
    """

    serializer_class = FilterOverrideSerializer
    queryset = FilterOverride.objects.all()
