import secrets
import unittest.mock

from django.test import TestCase
from django.utils import timezone

from pydis_site.apps.forms import authentication
from pydis_site.apps.forms import models


def fake_user() -> models.DiscordUser:
    """Return a fake user for testing."""
    return models.DiscordUser(
        id=1234,
        username="Joe 'CIA' Banks",
        discriminator=1234,
        avatar=None,
        bot=True,
        system=True,
        locale="tr",
        verified=False,
        email="shredder@jeremiahboby.me",
        flags=0,
    )


def fake_member(user: models.DiscordUser, role_ids: tuple[int, ...]) -> models.DiscordMember:
    """Return a fake member for testing."""
    return models.DiscordMember(
        user=user,
        roles=role_ids,
        joined_at=timezone.now(),
        deaf=True,
        mute=False,
    )


class AuthenticatedTestCase(TestCase):
    """Allows testing the forms API as an authenticated user."""

    authenticate_as_admin = False
    """Whether to authenticate the test member as an administrator."""

    roles: tuple[str, ...] = ()
    """Which Discord role names to return for the given user."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the user as configured for authentication."""
        cls.user = fake_user()
        cls.user.save()
        cls.addClassCleanup(cls.user.delete)

        roles_with_ids = tuple(models.DiscordRole(id=idx, name=name) for idx, name in enumerate(cls.roles))
        role_ids = tuple(role.id for role in roles_with_ids)
        cls.member = fake_member(cls.user, role_ids)
        cls.member.save()
        cls.addClassCleanup(cls.member.delete)

        get_roles_patcher = unittest.mock.patch("pydis_site.apps.forms.discord.get_roles")
        cls.patched_get_roles = get_roles_patcher.start()
        cls.patched_get_roles.return_value = roles_with_ids
        cls.addClassCleanup(get_roles_patcher.stop)

        if cls.authenticate_as_admin:
            admin = models.Admin(id=cls.member.id)
            admin.save()
            cls.addClassCleanup(admin.delete)

        cls.jwt_cookie = cls.create_jwt_cookie(cls.member)
        super().setUpClass()

    def setUp(self) -> None:
        """Log the user in to the test client."""
        self.jwt_login(self.member)
        super().setUp()

    @staticmethod
    def create_jwt_cookie(member: models.DiscordMember) -> str:
        """Create a cookie as expected by the forms authentication."""
        data = {
            "token": secrets.token_urlsafe(6),
            "refresh": secrets.token_urlsafe(6),
            "user_details": {
                "id": member.id,
                "name": member.user.username,
            },
        }
        return "JWT " + authentication.encode_jwt(data)

    def jwt_login(self, member: models.DiscordMember) -> None:
        """Log the user in to the test client."""
        self.client.cookies["token"] = self.jwt_cookie
