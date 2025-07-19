"""Custom authentication for the forms backend."""

import typing

import jwt
from django.conf import settings
from django.http import HttpRequest
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from . import discord
from . import models


def encode_jwt(info: dict, *, signing_secret_key: str = settings.SECRET_KEY) -> str:
    """Encode JWT information with either the configured signing key or a passed one."""
    return jwt.encode(info, signing_secret_key, algorithm="HS256")


class FormsUser:
    """Stores authentication information for a forms user."""

    # This allows us to safely use the same checks that we could use on a Django user.
    is_authenticated: bool = True

    def __init__(
        self,
        token: str,
        payload: dict[str, typing.Any],
        member: models.DiscordMember | None,
    ) -> None:
        """Set up a forms user."""
        self.token = token
        self.payload = payload
        self.admin = False
        self.member = member

    @property
    def display_name(self) -> str:
        """Return username and discriminator as display name."""
        return f"{self.payload['username']}#{self.payload['discriminator']}"

    @property
    def discord_mention(self) -> str:
        """Return a mention for this user on Discord."""
        return f"<@{self.payload['id']}>"

    @property
    def user_id(self) -> str:
        """Return this user's ID as a string."""
        return str(self.payload["id"])

    @property
    def decoded_token(self) -> dict[str, any]:
        """Decode the information stored in this user's JWT token."""
        return jwt.decode(self.token, settings.SECRET_KEY, algorithms=["HS256"])

    def get_roles(self) -> tuple[str, ...]:
        """Get a tuple of the user's discord roles by name."""
        if not self.member:
            return []

        server_roles = discord.get_roles()
        roles = [role.name for role in server_roles if role.id in self.member.roles]

        if "admin" in roles:
            # Protect against collision with the forms admin role
            roles.remove("admin")
            roles.append("discord admin")

        return tuple(roles)

    def is_admin(self) -> bool:
        """Return whether this user is an administrator."""
        self.admin = models.Admin.objects.filter(id=self.payload["id"]).exists()
        return self.admin

    def refresh_data(self) -> None:
        """Fetches user data from discord, and updates the instance."""
        self.member = discord.get_member(self.payload["id"])

        if self.member:
            self.payload = self.member.user.dict()
        else:
            self.payload = discord.fetch_user_details(self.decoded_token.get("token"))

        updated_info = self.decoded_token
        updated_info["user_details"] = self.payload

        self.token = encode_jwt(updated_info)


class AuthenticationResult(typing.NamedTuple):
    """Return scopes that the user has authenticated with."""

    scopes: tuple[str, ...]


# See https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
class JWTAuthentication(BaseAuthentication):
    """Custom DRF authentication backend for JWT."""

    @staticmethod
    def get_token_from_cookie(cookie: str) -> str:
        """Parse JWT token from cookie."""
        try:
            prefix, token = cookie.split()
        except ValueError:
            msg = "Unable to split prefix and token from authorization cookie."
            raise AuthenticationFailed(msg)

        if prefix.upper() != "JWT":
            msg = f"Invalid authorization cookie prefix '{prefix}'."
            raise AuthenticationFailed(msg)

        return token

    def authenticate(
        self,
        request: HttpRequest,
    ) -> tuple[FormsUser, None] | None:
        """Handles JWT authentication process."""
        cookie = request.COOKIES.get("token")
        if not cookie:
            return None

        token = self.get_token_from_cookie(cookie)

        try:
            # New key.
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            try:
                # Old key. Should be removed at a certain point.
                payload = jwt.decode(token, settings.FORMS_SECRET_KEY, algorithms=["HS256"])
            except jwt.InvalidTokenError as e:
                raise AuthenticationFailed(str(e))

        scopes = ["authenticated"]

        if not payload.get("token"):
            msg = "Token is missing from JWT."
            raise AuthenticationFailed(msg)
        if not payload.get("refresh"):
            msg = "Refresh token is missing from JWT."
            raise AuthenticationFailed(msg)

        try:
            user_details = payload.get("user_details")
            if not user_details or not user_details.get("id"):
                msg = "Improper user details."
                raise AuthenticationFailed(msg)
        except Exception:
            msg = "Could not parse user details."
            raise AuthenticationFailed(msg)

        user = FormsUser(
            token,
            user_details,
            discord.get_member(user_details["id"]),
        )
        if user.is_admin():
            scopes.append("admin")

        scopes.extend(user.get_roles())

        return user, AuthenticationResult(scopes=tuple(scopes))
