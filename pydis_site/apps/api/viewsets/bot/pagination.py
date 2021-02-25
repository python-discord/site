from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class LimitSetPagination(LimitOffsetPagination):
    """Extend LimitOffsetPagination."""

    default_limit = 100

    def get_paginated_response(self, data: list) -> Response:
        """Override default response."""
        return Response(data)
