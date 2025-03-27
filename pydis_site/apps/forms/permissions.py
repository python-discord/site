from typing import Iterable

from rest_framework.permissions import BasePermission


class HasJWTScopes(BasePermission):
    """Ensure that requesting users have the JWT scopes specified in the constructor."""

    def __init__(self, scopes: Iterable[str]) -> None:
        self.scopes = frozenset(scopes)

    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated and request.auth and frozenset(request.auth.scopes) == self.scopes
