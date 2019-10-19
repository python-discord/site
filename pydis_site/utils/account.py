from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.contrib.messages import ERROR, add_message
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse


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
            add_message(
                request, ERROR,
                "You must login with Discord before connecting another account. Your account "
                "details have not been saved."
            )

            raise ImmediateHttpResponse(redirect(reverse("home")))

        return True
