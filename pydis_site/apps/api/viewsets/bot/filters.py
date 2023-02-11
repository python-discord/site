from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot.filters import (  # noqa: I101 - Preserving the filter order
    FilterList,
    Filter
)
from pydis_site.apps.api.serializers import (  # noqa: I101 - Preserving the filter order
    FilterListSerializer,
    FilterSerializer,
)


class FilterListViewSet(ModelViewSet):
    """
    View providing GET/DELETE on lists of items allowed or denied by our bot.

    ## Routes
    ### GET /bot/filter/filter_lists
    Returns all FilterList items in the database.

    #### Response format
    >>> [
    ...     {
    ...         "id": 1,
    ...         "created_at": "2023-01-27T21:26:34.027293Z",
    ...         "updated_at": "2023-01-27T21:26:34.027308Z",
    ...         "name": "invite",
    ...         "list_type": 1,
    ...         "filters": [
    ...             {
    ...                 "id": 1,
    ...                 "created_at": "2023-01-27T21:26:34.029539Z",
    ...                 "updated_at": "2023-01-27T21:26:34.030532Z",
    ...                 "content": "267624335836053506",
    ...                 "description": "Python Discord",
    ...                 "additional_field": None,
    ...                 "filter_list": 1,
    ...                 "settings": {
    ...                     "bypass_roles": None,
    ...                     "filter_dm": None,
    ...                     "enabled": None,
    ...                     "remove_context": None,
    ...                     "send_alert": None,
    ...                     "infraction_and_notification": {
    ...                         "infraction_type": None,
    ...                         "infraction_reason": None,
    ...                         "infraction_duration": None,
    ...                         "infraction_channel": None,
    ...                         "dm_content": None,
    ...                         "dm_embed": None
    ...                     },
    ...                     "channel_scope": {
    ...                         "disabled_channels": None,
    ...                         "disabled_categories": None,
    ...                         "enabled_channels": None,
    ...                         "enabled_categories": None
    ...                     },
    ...                     "mentions": {
    ...                         "guild_pings": None,
    ...                         "dm_pings": None
    ...                     }
    ...                 }
    ...             },
    ...             ...
    ...         ],
    ...         "settings": {
    ...             "bypass_roles": [
    ...                 "Helpers"
    ...             ],
    ...             "filter_dm": True,
    ...             "enabled": True,
    ...             "remove_context": True,
    ...             "send_alert": True,
    ...             "infraction_and_notification": {
    ...                 "infraction_type": "NONE",
    ...                 "infraction_reason": "",
    ...                 "infraction_duration": "0.0",
    ...                 "infraction_channel": 0,
    ...                 "dm_content": "Per Rule 6, your invite link has been removed...",
    ...                 "dm_embed": ""
    ...             },
    ...             "channel_scope": {
    ...                 "disabled_channels": [],
    ...                 "disabled_categories": [
    ...                     "CODE JAM"
    ...                 ],
    ...                 "enabled_channels": [],
    ...                 "enabled_categories": []
    ...             },
    ...             "mentions": {
    ...                 "guild_pings": [
    ...                     "Moderators"
    ...                 ],
    ...                 "dm_pings": []
    ...             }
    ...         }
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
    ...     "created_at": "2023-01-27T21:26:34.027293Z",
    ...     "updated_at": "2023-01-27T21:26:34.027308Z",
    ...     "name": "invite",
    ...     "list_type": 1,
    ...     "filters": [
    ...         {
    ...             "id": 1,
    ...             "created_at": "2023-01-27T21:26:34.029539Z",
    ...             "updated_at": "2023-01-27T21:26:34.030532Z",
    ...             "content": "267624335836053506",
    ...             "description": "Python Discord",
    ...             "additional_field": None,
    ...             "filter_list": 1,
    ...             "settings": {
    ...                 "bypass_roles": None,
    ...                 "filter_dm": None,
    ...                 "enabled": None,
    ...                 "remove_context": None,
    ...                 "send_alert": None,
    ...                 "infraction_and_notification": {
    ...                     "infraction_type": None,
    ...                     "infraction_reason": None,
    ...                     "infraction_duration": None,
    ...                     "infraction_channel": None,
    ...                     "dm_content": None,
    ...                     "dm_embed": None
    ...                 },
    ...                 "channel_scope": {
    ...                     "disabled_channels": None,
    ...                     "disabled_categories": None,
    ...                     "enabled_channels": None,
    ...                     "enabled_categories": None
    ...                 },
    ...                 "mentions": {
    ...                     "guild_pings": None,
    ...                     "dm_pings": None
    ...                 }
    ...             }
    ...         },
    ...         ...
    ...     ],
    ...     "settings": {
    ...         "bypass_roles": [
    ...             "Helpers"
    ...         ],
    ...         "filter_dm": True,
    ...         "enabled": True,
    ...         "remove_context": True,
    ...         "send_alert": True,
    ...         "infraction_and_notification": {
    ...             "infraction_type": "NONE",
    ...             "infraction_reason": "",
    ...             "infraction_duration": "0.0",
    ...             "infraction_channel": 0,
    ...             "dm_content": "Per Rule 6, your invite link has been removed...",
    ...             "dm_embed": ""
    ...         },
    ...         "channel_scope": {
    ...             "disabled_channels": [],
    ...             "disabled_categories": [
    ...                 "CODE JAM"
    ...             ],
    ...             "enabled_channels": [],
    ...             "enabled_categories": []
    ...         },
    ...         "mentions": {
    ...             "guild_pings": [
    ...                 "Moderators"
    ...             ],
    ...             "dm_pings": []
    ...         }
    ...     }
    ... }

    #### Status codes
    - 200: returned on success
    - 404: returned if the id was not found.

    ### POST /bot/filter/filter_lists
    Adds a single FilterList item to the database.

    #### Request body
    >>> {
    ...     "name": "invite",
    ...     "list_type": 1,
    ...     "bypass_roles": [
    ...         "Helpers"
    ...     ],
    ...     "filter_dm": True,
    ...     "enabled": True,
    ...     "remove_context": True,
    ...     "send_alert": True,
    ...     "infraction_type": "NONE",
    ...     "infraction_reason": "",
    ...     "infraction_duration": "0.0",
    ...     "infraction_channel": 0,
    ...     "dm_content": "Per Rule 6, your invite link has been removed...",
    ...     "dm_embed": "",
    ...     "disabled_channels": [],
    ...     "disabled_categories": [
    ...         "CODE JAM"
    ...     ],
    ...     "enabled_channels": [],
    ...     "enabled_categories": []
    ...     "guild_pings": [
    ...         "Moderators"
    ...     ],
    ...     "dm_pings": []
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if one of the given fields is invalid

    ### PATCH /bot/filter/filter_lists/<id:int>
    Updates a specific FilterList item from the database.

    #### Response format
    >>> {
    ...     "id": 1,
    ...     "created_at": "2023-01-27T21:26:34.027293Z",
    ...     "updated_at": "2023-01-27T21:26:34.027308Z",
    ...     "name": "invite",
    ...     "list_type": 1,
    ...     "filters": [
    ...         {
    ...             "id": 1,
    ...             "created_at": "2023-01-27T21:26:34.029539Z",
    ...             "updated_at": "2023-01-27T21:26:34.030532Z",
    ...             "content": "267624335836053506",
    ...             "description": "Python Discord",
    ...             "additional_field": None,
    ...             "filter_list": 1,
    ...             "settings": {
    ...                 "bypass_roles": None,
    ...                 "filter_dm": None,
    ...                 "enabled": None,
    ...                 "remove_context": None,
    ...                 "send_alert": None,
    ...                 "infraction_and_notification": {
    ...                     "infraction_type": None,
    ...                     "infraction_reason": None,
    ...                     "infraction_duration": None,
    ...                     "infraction_channel": None,
    ...                     "dm_content": None,
    ...                     "dm_embed": None
    ...                 },
    ...                 "channel_scope": {
    ...                     "disabled_channels": None,
    ...                     "disabled_categories": None,
    ...                     "enabled_channels": None,
    ...                     "enabled_categories": None
    ...                 },
    ...                 "mentions": {
    ...                     "guild_pings": None,
    ...                     "dm_pings": None
    ...                 }
    ...             }
    ...         },
    ...         ...
    ...     ],
    ...     "settings": {
    ...         "bypass_roles": [
    ...             "Helpers"
    ...         ],
    ...         "filter_dm": True,
    ...         "enabled": True,
    ...         "remove_context": True,
    ...         "send_alert": True,
    ...         "infraction_and_notification": {
    ...             "infraction_type": "NONE",
    ...             "infraction_reason": "",
    ...             "infraction_duration": "0.0",
    ...             "infraction_channel": 0,
    ...             "dm_content": "Per Rule 6, your invite link has been removed...",
    ...             "dm_embed": ""
    ...         },
    ...         "channel_scope": {
    ...             "disabled_channels": [],
    ...             "disabled_categories": [
    ...                 "CODE JAM"
    ...             ],
    ...             "enabled_channels": [],
    ...             "enabled_categories": []
    ...         },
    ...         "mentions": {
    ...             "guild_pings": [
    ...                 "Moderators"
    ...             ],
    ...             "dm_pings": []
    ...         }
    ...     }
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if one of the given fields is invalid

    ### DELETE /bot/filter/filter_lists/<id:int>
    Deletes the FilterList item with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a FilterList with the given `id` does not exist
    """

    serializer_class = FilterListSerializer
    queryset = FilterList.objects.all()


class FilterViewSet(ModelViewSet):
    """
    View providing CRUD operations on items allowed or denied by our bot.

    ## Routes
    ### GET /bot/filter/filters
    Returns all Filter items in the database.

    #### Response format
    >>> [
    ...         {
    ...         "id": 1,
    ...         "created_at": "2023-01-27T21:26:34.029539Z",
    ...         "updated_at": "2023-01-27T21:26:34.030532Z",
    ...         "content": "267624335836053506",
    ...         "description": "Python Discord",
    ...         "additional_field": None,
    ...         "filter_list": 1,
    ...         "settings": {
    ...             "bypass_roles": None,
    ...             "filter_dm": None,
    ...             "enabled": None,
    ...             "remove_context": None,
    ...             "send_alert": None,
    ...             "infraction_and_notification": {
    ...                 "infraction_type": None,
    ...                 "infraction_reason": None,
    ...                 "infraction_duration": None,
    ...                 "infraction_channel": None,
    ...                 "dm_content": None,
    ...                 "dm_embed": None
    ...             },
    ...             "channel_scope": {
    ...                 "disabled_channels": None,
    ...                 "disabled_categories": None,
    ...                 "enabled_channels": None,
    ...                 "enabled_categories": None
    ...             },
    ...             "mentions": {
    ...                 "guild_pings": None,
    ...                 "dm_pings": None
    ...             }
    ...         }
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
    ...     "created_at": "2023-01-27T21:26:34.029539Z",
    ...     "updated_at": "2023-01-27T21:26:34.030532Z",
    ...     "content": "267624335836053506",
    ...     "description": "Python Discord",
    ...     "additional_field": None,
    ...     "filter_list": 1,
    ...     "settings": {
    ...         "bypass_roles": None,
    ...         "filter_dm": None,
    ...         "enabled": None,
    ...         "remove_context": None,
    ...         "send_alert": None,
    ...         "infraction_and_notification": {
    ...             "infraction_type": None,
    ...             "infraction_reason": None,
    ...             "infraction_duration": None,
    ...             "infraction_channel": None,
    ...             "dm_content": None,
    ...             "dm_embed": None
    ...         },
    ...         "channel_scope": {
    ...             "disabled_channels": None,
    ...             "disabled_categories": None,
    ...             "enabled_channels": None,
    ...             "enabled_categories": None
    ...         },
    ...         "mentions": {
    ...             "guild_pings": None,
    ...             "dm_pings": None
    ...         }
    ...     }
    ... }

    #### Status codes
    - 200: returned on success
    - 404: returned if the id was not found.

    ### POST /bot/filter/filters
    Adds a single Filter item to the database.

    #### Request body
    >>> {
    ...     "filter_list": 1,
    ...     "content": "267624335836053506",
    ...     "description": "Python Discord",
    ...     "additional_field": None,
    ...     "bypass_roles": None,
    ...     "filter_dm": None,
    ...     "enabled": False,
    ...     "remove_context": None,
    ...     "send_alert": None,
    ...     "infraction_type": None,
    ...     "infraction_reason": None,
    ...     "infraction_duration": None,
    ...     "infraction_channel": None,
    ...     "dm_content": None,
    ...     "dm_embed": None
    ...     "disabled_channels": None,
    ...     "disabled_categories": None,
    ...     "enabled_channels": None,
    ...     "enabled_categories": None
    ...     "guild_pings": None,
    ...     "dm_pings": None
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if one of the given fields is invalid

    ### PATCH /bot/filter/filters/<id:int>
    Updates a specific Filter item from the database.

    #### Response format
    >>> {
    ...     "id": 1,
    ...     "created_at": "2023-01-27T21:26:34.029539Z",
    ...     "updated_at": "2023-01-27T21:26:34.030532Z",
    ...     "content": "267624335836053506",
    ...     "description": "Python Discord",
    ...     "additional_field": None,
    ...     "filter_list": 1,
    ...     "settings": {
    ...         "bypass_roles": None,
    ...         "filter_dm": None,
    ...         "enabled": None,
    ...         "remove_context": None,
    ...         "send_alert": None,
    ...         "infraction_and_notification": {
    ...             "infraction_type": None,
    ...             "infraction_reason": None,
    ...             "infraction_duration": None,
    ...             "infraction_channel": None,
    ...             "dm_content": None,
    ...             "dm_embed": None
    ...         },
    ...         "channel_scope": {
    ...             "disabled_channels": None,
    ...             "disabled_categories": None,
    ...             "enabled_channels": None,
    ...             "enabled_categories": None
    ...         },
    ...         "mentions": {
    ...             "guild_pings": None,
    ...             "dm_pings": None
    ...         }
    ...     }
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if one of the given fields is invalid

    ### DELETE /bot/filter/filters/<id:int>
    Deletes the Filter item with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a Filter with the given `id` does not exist
    """

    serializer_class = FilterSerializer
    queryset = Filter.objects.all()
