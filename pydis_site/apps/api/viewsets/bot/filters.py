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
    ...         "name": "invites",
    ...         "list_type": 1,
    ...         "filters": [
    ...             {
    ...                 "id": 1,
    ...                 "content": "267624335836053506",
    ...                 "description": "Python Discord",
    ...                 "additional_field": None,
    ...                 "filter_list": 1
    ...                 "settings": {
    ...                        "bypass_roles": None
    ...                        "filter_dm": None,
    ...                        "enabled": None
    ...                        "send_alert": True,
    ...                        "delete_messages": None
    ...                        "infraction_and_notification": {
    ...                            "infraction_type": None,
    ...                            "infraction_reason": "",
    ...                            "infraction_duration": None
    ...                            "dm_content": None,
    ...                            "dm_embed": None
    ...                        },
    ...                        "channel_scope": {
    ...                            "disabled_channels": None,
    ...                            "disabled_categories": None,
    ...                            "enabled_channels": None
    ...                        }
    ...                        "mentions": {
    ...                            "ping_type": None
    ...                            "dm_ping_type": None
    ...                         }
    ...                    }
    ...
    ...             },
    ...             ...
    ...         ],
    ...            "settings": {
    ...              "bypass_roles": [
    ...                  "staff"
    ...              ],
    ...              "filter_dm": True,
    ...              "enabled": True
    ...              "delete_messages": True,
    ...              "send_alert": True
    ...              "infraction_and_notification": {
    ...                   "infraction_type": "",
    ...                   "infraction_reason": "",
    ...                   "infraction_duration": "0.0",
    ...                   "dm_content": "",
    ...                   "dm_embed": ""
    ...               }
    ...               "channel_scope": {
    ...                 "disabled_channels": [],
    ...                 "disabled_categories": [],
    ...                 "enabled_channels": []
    ...               }
    ...               "mentions": {
    ...                 "ping_type": [
    ...                     "onduty"
    ...                 ]
    ...                 "dm_ping_type": []
    ...                }
    ...           },
    ...     ...
    ... ]

    #### Status codes
    - 200: returned on success
    - 401: returned if unauthenticated

    ### GET /bot/filter/filter_lists/<id:int>
    Returns a specific FilterList item from the database.

    #### Response format
    >>> {
    ...         "id": 1,
    ...         "name": "invites",
    ...         "list_type": 1,
    ...         "filters": [
    ...             {
    ...                 "id": 1,
    ...                 "filter_list": 1
    ...                 "content": "267624335836053506",
    ...                 "description": "Python Discord",
    ...                 "additional_field": None,
    ...                 "settings": {
    ...                        "bypass_roles": None
    ...                        "filter_dm": None,
    ...                        "enabled": None
    ...                        "delete_messages": None,
    ...                        "send_alert": None
    ...                        "infraction_and_notification": {
    ...                            "infraction_type": None,
    ...                            "infraction_reason": "",
    ...                            "infraction_duration": None
    ...                            "dm_content": None,
    ...                            "dm_embed": None
    ...                        },
    ...                        "channel_scope": {
    ...                            "disabled_channels": None,
    ...                            "disabled_categories": None,
    ...                            "enabled_channels": None
    ...                        }
    ...                        "mentions": {
    ...                            "ping_type": None
    ...                            "dm_ping_type": None
    ...                         }
    ...                    }
    ...
    ...             },
    ...             ...
    ...         ],
    ...            "settings": {
    ...              "bypass_roles": [
    ...                  "staff"
    ...              ],
    ...              "filter_dm": True,
    ...              "enabled": True
    ...              "delete_messages": True
    ...              "send_alert": True
    ...              "infraction_and_notification": {
    ...                   "infraction_type": "",
    ...                   "infraction_reason": "",
    ...                   "infraction_duration": "0.0",
    ...                   "dm_content": "",
    ...                   "dm_embed": ""
    ...               }
    ...               "channel_scope": {
    ...                 "disabled_channels": [],
    ...                 "disabled_categories": [],
    ...                 "enabled_channels": []
    ...                }
    ...               "mentions": {
    ...                 "ping_type": [
    ...                     "onduty"
    ...                 ]
    ...                 "dm_ping_type": []
    ...                }
    ... }

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
    ...                        "bypass_roles": None
    ...                        "filter_dm": None,
    ...                        "enabled": None
    ...                        "delete_messages": True,
    ...                        "send_alert": True
    ...                        "infraction": {
    ...                            "infraction_type": None,
    ...                            "infraction_reason": None,
    ...                            "infraction_duration": None
    ...                        },
    ...                        "channel_scope": {
    ...                          "disabled_channels": None,
    ...                          "disabled_categories": None,
    ...                          "enabled_channels": None
    ...                        }
    ...                        "mentions": {
    ...                          "ping_type": None,
    ...                          "dm_ping_type": None
    ...                       }
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
    ...                        "bypass_roles": None
    ...                        "filter_dm": None,
    ...                        "enabled": None
    ...                        "delete_messages": True,
    ...                        "send_alert": True
    ...                        "infraction": {
    ...                            "infraction_type": None,
    ...                            "infraction_reason": None,
    ...                            "infraction_duration": None
    ...                        },
    ...                        "channel_scope": {
    ...                          "disabled_channels": None,
    ...                          "disabled_categories": None,
    ...                          "enabled_channels": None,
    ...                        }
    ...                       "mentions": {
    ...                         "ping_type": None
    ...                         "dm_ping_type": None
    ...                       }
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
