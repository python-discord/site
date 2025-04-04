from collections.abc import Iterable

from django.request import HttpRequest
from django.views import View
from rest_framework.permissions import BasePermission


class HasJWTScopes(BasePermission):
    """Ensure that requesting users have the JWT scopes specified in the constructor."""

    def __init__(self, scopes: Iterable[str]) -> None:
        """Configure the required scopes to access a resource."""
        self.scopes = frozenset(scopes)

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        """Only allow authenticated users with the configured set of scopes to access this resource."""
        # XXX: this should check for superset, not strict equality.
        return request.user.is_authenticated and request.auth and frozenset(request.auth.scopes) == self.scopes
