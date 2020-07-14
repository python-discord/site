from typing import Any, Dict

from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.contrib.auth.models import User as DjangoUser
from django.contrib.messages import ERROR, add_message
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from pydis_site.apps.api.models import User as DiscordUser

ERROR_CONNECT_DISCORD = ("You must login with Discord before connecting another account. "
                         "Your account details have not been saved.")
ERROR_JOIN_DISCORD = ("Please join the Discord server and verify that you accept the rules and "
                      "privacy policy.")


class AccountAdapter(DefaultAccountAdapter):
    """An Allauth account adapter that prevents signups via form submission."""

    def is_open_for_signup(self, request: HttpRequest) -> bool:
        """
        Checks whether or not the site is open for signups.

        We override this to always return False so that users may never sign up using
        Allauth's signup form endpoints, to be on the safe side - since we only want users
        to sign up using their Discord account.
        """
        return False


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """An Allauth SocialAccount adapter that prevents signups via non-Discord connections."""

    def is_open_for_signup(self, request: HttpRequest, social_login: SocialLogin) -> bool:
        """
        Checks whether or not the site is open for signups.

        We override this method in order to prevent users from creating a new account using
        a non-Discord connection, as we require this connection for our users.
        """
        if social_login.account.provider != "discord":
            add_message(request, ERROR, ERROR_CONNECT_DISCORD)

            raise ImmediateHttpResponse(redirect(reverse("home")))

        try:
            user = DiscordUser.objects.get(id=int(social_login.account.uid))
        except DiscordUser.DoesNotExist:
            add_message(request, ERROR, ERROR_JOIN_DISCORD)

            raise ImmediateHttpResponse(redirect(reverse("home")))

        if len(user.roles) <= 1:
            add_message(request, ERROR, ERROR_JOIN_DISCORD)

            raise ImmediateHttpResponse(redirect(reverse("home")))

        return True

    def populate_user(self, request: HttpRequest,
                      social_login: SocialLogin,
                      data: Dict[str, Any]) -> DjangoUser:
        """
        Method used to populate a Django User with data.

        We override this so that the Django user is created with the username#discriminator,
        instead of just the username, as Django users must have unique usernames. For display
        purposes, we also set the `name` key, which is used for `first_name` in the database.
        """
        if social_login.account.provider == "discord":
            discriminator = social_login.account.extra_data["discriminator"]
            data["username"] = f"{data['username']}#{discriminator:0>4}"
            data["name"] = data["username"]

        return super().populate_user(request, social_login, data)
