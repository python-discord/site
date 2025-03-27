"""API functions for Discord access."""

import httpx
from django.conf import settings

from . import models
from . import util


__all__ = ("get_member", "get_roles")


def fetch_and_update_roles() -> tuple[models.DiscordRole, ...]:
    """Get information about roles from Discord."""
    with httpx.Client() as client:
        r = client.get(
            f"{settings.DISCORD_API_BASE_URL}/guilds/{settings.DISCORD_GUILD_ID}/roles",
            headers={"Authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
        )

        r.raise_for_status()
        return tuple(models.DiscordRole(**role) for role in r.json())


def fetch_member_details(member_id: int) -> models.DiscordMember | None:
    """Get a member by ID from the configured guild using the discord API."""
    with httpx.Client() as client:
        r = client.get(
            f"{settings.DISCORD_API_BASE_URL}/guilds/{settings.DISCORD_GUILD_ID}/members/{member_id}",
            headers={"Authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"},
        )

        if r.status_code == 404:
            return None

        r.raise_for_status()
        return models.DiscordMember(**r.json())


def fetch_user_details(bearer_token: str) -> dict:
    """Fetch information about the Discord user associated with the given ``bearer_token``."""
    with httpx.Client() as client:
        r = client.get(
            f"{settings.DISCORD_API_BASE_URL}/users/@me",
            headers={
                "Authorization": f"Bearer {bearer_token}",
            },
        )

        r.raise_for_status()

        return r.json()


def fetch_bearer_token(code: str, redirect: str, *, refresh: bool) -> dict:
    """
    Fetch an OAuth2 bearer token.

    ## Arguments

    - ``code``: The code or refresh token for the operation. Usually provided by Discord.
    - ``redirect``: Where to redirect the client after successful login.

    ## Keyword arguments

    - ``refresh``: Whether to fetch a refresh token.
    """
    with httpx.Client() as client:
        data = {
            "client_id": settings.DISCORD_OAUTH2_CLIENT_ID,
            "client_secret": settings.DISCORD_OAUTH2_CLIENT_SECRET,
            "redirect_uri": f"{redirect}/callback",
        }

        if refresh:
            data["grant_type"] = "refresh_token"
            data["refresh_token"] = code
        else:
            data["grant_type"] = "authorization_code"
            data["code"] = code

        r = client.post(
            f"{settings.DISCORD_API_BASE_URL}/oauth2/token",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data=data,
        )

        r.raise_for_status()

        return r.json()


def get_roles(*, force_refresh: bool = False, stale_after: int = 60 * 60 * 24) -> tuple[models.DiscordRole, ...]:
    """
    Get a tuple of all roles from the cache, or discord API if not available.

    ## Keyword arguments

    - `force_refresh` (`bool`): Skip the cache and always update the roles from
      Discord.
    - `stale_after` (`int`): Seconds after which to consider the stored roles
      as stale and to refresh them.
    """
    if not force_refresh:
        roles = models.DiscordRole.objects.all()
        oldest = min(role.last_update for role in roles)
        if not util.is_stale(oldest, 60 * 60 * 24):  # 1 day
            return tuple(roles)

    return fetch_and_update_roles()


def get_member(
    user_id: int,
    *,
    force_refresh: bool = False,
) -> models.DiscordMember | None:
    """
    Get a member from the cache, or from the discord API.

    ## Keyword arguments

    - `force_refresh` (`bool`): Skip the cache and always update the roles from
      Discord.
    - `stale_after` (`int`): Seconds after which to consider the stored roles
      as stale and to refresh them.

    ## Return value

    Returns `None` if the member object does not exist.
    """
    if not force_refresh:
        member = models.DiscordMember.objects.get(id=user_id)
        if not util.is_stale(member.last_update, 60 * 60):
            return member

    member = fetch_member_details(user_id)
    if member:
        member.save()

    return member
