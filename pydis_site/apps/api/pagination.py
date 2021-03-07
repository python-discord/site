import typing

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class LimitOffsetPaginationExtended(LimitOffsetPagination):
    """
    Extend LimitOffsetPagination to customise the default response.

    For example:

    ## Default response
            {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [{
                        "id": 6,
                        "inserted_at": "2021-01-26T21:13:35.477879Z",
                        "expires_at": null,
                        "active": false,
                        "user": 1,
                        "actor": 2,
                        "type": "warning",
                        "reason": null,
                        "hidden": false
                    }]
            }
    ## Required response
            [{
                "id": 6,
                "inserted_at": "2021-01-26T21:13:35.477879Z",
                "expires_at": null,
                "active": false,
                "user": 1,
                "actor": 2,
                "type": "warning",
                "reason": null,
                "hidden": false
            }]

    """

    default_limit = 100

    def get_paginated_response(self, data: typing.Any) -> Response:
        """Override to skip metadata i.e. `count`, `next`, and `previous`."""
        return Response(data)
