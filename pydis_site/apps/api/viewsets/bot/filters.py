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
    ...         "name": "guild_invite",
    ...         "list_type": 1,
    ...         "filters": [
    ...             {
    ...                 "id": 1,
    ...                 "filter_list": 1
    ...                 "content": "267624335836053506",
    ...                 "description": "Python Discord",
    ...                 "additional_field": None,
    ...                 "settings": {
    ...                        "ping_type": None,
    ...                        "dm_ping_type": None
    ...                        "bypass_roles": None
    ...                        "filter_dm": None,
    ...                        "enabled": False
    ...                        "delete_messages": True
    ...                        "infraction": {
    ...                            "infraction_type": None,
    ...                            "infraction_reason": "",
    ...                            "infraction_duration": None
    ...                        },
    ...                        "channel_scope": {
    ...                            "allowed_channels": None,
    ...                            "allowed_categories": None,
    ...                            "disallowed_channels": None,
    ...                            "disallowed_categories": None
    ...                        }
    ...                    }
    ...
    ...             },
    ...             ...
    ...         ],
    ...            "settings": {
    ...              "ping_type": [
    ...                  "onduty"
    ...              ],
    ...              "dm_ping_type": [
    ...                  "onduty"
    ...              ],
    ...              "bypass_roles": [
    ...                  267630620367257601
    ...              ],
    ...              "filter_dm": True,
    ...              "enabled": False
    ...              "delete_messages": True
    ...              "infraction": {
    ...                   "infraction_type": None,
    ...                   "infraction_reason": "",
    ...                   "infraction_duration": None,
    ...               }
    ...              "channel_scope": {
    ...                "disallowed_channels": [],
    ...                "disallowed_categories": [],
    ...                "allowed_channels": [],
    ...                "allowed_categories": []
    ...               }
    ...           }

    #### Status codes
    - 200: returned on success
    - 401: returned if unauthenticated

    ### GET /bot/filter/filter_lists/<id:int>
    Returns a specific FilterList item from the database.

    #### Response format
    >>>
    ...     {
    ...         "id": 1,
    ...         "name": "guild_invite",
    ...         "list_type": 1,
    ...         "filters": [
    ...             {
    ...                 "id": 1,
    ...                 "filter_list": 1
    ...                 "content": "267624335836053506",
    ...                 "description": "Python Discord",
    ...                 "additional_field": None,
    ...                 "settings": {
    ...                        "ping_type": None,
    ...                        "dm_ping_type": None
    ...                        "bypass_roles": None
    ...                        "filter_dm": None,
    ...                        "enabled": False
    ...                        "delete_messages": True
    ...                        "infraction": {
    ...                            "infraction_type": None,
    ...                            "infraction_reason": "",
    ...                            "infraction_duration": None
    ...                        },
    ...                        "channel_scope": {
    ...                            "allowed_channels": None,
    ...                            "allowed_categories": None,
    ...                            "disallowed_channels": None,
    ...                            "disallowed_categories": None
    ...                        }
    ...                    }
    ...
    ...             },
    ...
    ...         ],
    ...            "settings": {
    ...              "ping_type": [
    ...                  "onduty"
    ...              ],
    ...              "dm_ping_type": [
    ...                  "onduty"
    ...              ],
    ...              "bypass_roles": [
    ...                  267630620367257601
    ...              ],
    ...              "filter_dm": True,
    ...              "enabled": False
    ...              "delete_messages": True
    ...              "infraction": {
    ...                   "infraction_type": None,
    ...                   "infraction_reason": "",
    ...                   "infraction_duration": None,
    ...               }
    ...              "channel_scope": {
    ...                "disallowed_channels": [],
    ...                "disallowed_categories": [],
    ...                "allowed_channels": [],
    ...                "allowed_categories": []
    ...               }
    ...           }
    ...       }

    #### Status codes
    - 200: returned on success
    - 404: returned if the id was not found.

    ### DELETE /bot/filter/filter_lists/<id:int>
    Deletes the FilterList item with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a tag with the given `id` does not exist
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
    ...     {
    ...                 "id": 1,
    ...                 "filter_list": 1
    ...                 "content": "267624335836053506",
    ...                 "description": "Python Discord",
    ...                 "additional_field": None,
    ...                 "settings": {
    ...                        "ping_type": None,
    ...                        "dm_ping_type": None
    ...                        "bypass_roles": None
    ...                        "filter_dm": None,
    ...                        "enabled": False
    ...                        "delete_messages": True
    ...                        "infraction": {
    ...                            "infraction_type": None,
    ...                            "infraction_reason": "",
    ...                            "infraction_duration": None
    ...                        },
    ...                        "channel_scope": {
    ...                            "allowed_channels": None,
    ...                            "allowed_categories": None,
    ...                            "disallowed_channels": None,
    ...                            "disallowed_categories": None
    ...                        }
    ...                    }
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
    ...                 "id": 1,
    ...                 "filter_list": 1
    ...                 "content": "267624335836053506",
    ...                 "description": "Python Discord",
    ...                 "additional_field": None,
    ...                 "settings": {
    ...                        "ping_type": None,
    ...                        "dm_ping_type": None
    ...                        "bypass_roles": None
    ...                        "filter_dm": None,
    ...                        "enabled": False
    ...                        "delete_messages": True
    ...                        "infraction": {
    ...                            "infraction_type": None,
    ...                            "infraction_reason": "",
    ...                            "infraction_duration": None
    ...                        },
    ...                        "channel_scope": {
    ...                            "allowed_channels": None,
    ...                            "allowed_categories": None,
    ...                            "disallowed_channels": None,
    ...                            "disallowed_categories": None
    ...                        }
    ...                    }
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
