"""Tests for the data migration in `filename`."""
import logging
from collections import ChainMap, namedtuple
from datetime import timedelta
from itertools import count
from typing import Dict, Iterable, Type, Union

from django.db.models import Q
from django.forms.models import model_to_dict
from django.utils import timezone

from pydis_site.apps.api.models import Infraction, User
from .base import MigrationsTestCase

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


InfractionHistory = namedtuple('InfractionHistory', ("user_id", "infraction_history"))


class InfractionFactory:
    """Factory that creates infractions for a User instance."""

    infraction_id = count(1)
    user_id = count(1)
    default_values = {
        'active': True,
        'expires_at': None,
        'hidden': False,
    }

    @classmethod
    def create(
        cls,
        actor: User,
        infractions: Iterable[Dict[str, Union[str, int, bool]]],
        infraction_model: Type[Infraction] = Infraction,
        user_model: Type[User] = User,
    ) -> InfractionHistory:
        """
        Creates `infractions` for the `user` with the given `actor`.

        The `infractions` dictionary can contain the following fields:
         - `type` (required)
         - `active` (default: True)
         - `expires_at` (default: None; i.e, permanent)
         - `hidden` (default: False).

        The parameters `infraction_model` and `user_model` can be used to pass in an instance of
        both model classes from a different migration/project state.
        """
        user_id = next(cls.user_id)
        user = user_model.objects.create(
            id=user_id,
            name=f"Infracted user {user_id}",
            discriminator=user_id,
            avatar_hash=None,
        )
        infraction_history = []

        for infraction in infractions:
            infraction = dict(infraction)
            infraction["id"] = next(cls.infraction_id)
            infraction = ChainMap(infraction, cls.default_values)
            new_infraction = infraction_model.objects.create(
                user=user,
                actor=actor,
                type=infraction["type"],
                reason=f"`{infraction['type']}` infraction (ID: {infraction['id']} of {user}",
                active=infraction['active'],
                hidden=infraction['hidden'],
                expires_at=infraction['expires_at'],
            )
            infraction_history.append(new_infraction)

        return InfractionHistory(user_id=user_id, infraction_history=infraction_history)


class InfractionFactoryTests(MigrationsTestCase):
    """Tests for the InfractionFactory."""

    app = "api"
    migration_prior = "0046_reminder_jump_url"
    migration_target = "0046_reminder_jump_url"

    @classmethod
    def setUpPostMigrationData(cls, apps):
        """Create a default actor for all infractions."""
        cls.infraction_model = apps.get_model('api', 'Infraction')
        cls.user_model = apps.get_model('api', 'User')

        cls.actor = cls.user_model.objects.create(
            id=9999,
            name="Unknown Moderator",
            discriminator=1040,
            avatar_hash=None,
        )

    def test_infraction_factory_total_count(self):
        """Does the test database hold as many infractions as we tried to create?"""
        InfractionFactory.create(
            actor=self.actor,
            infractions=(
                {'type': 'kick', 'active': False, 'hidden': False},
                {'type': 'ban', 'active': True, 'hidden': False},
                {'type': 'note', 'active': False, 'hidden': True},
            ),
            infraction_model=self.infraction_model,
            user_model=self.user_model,
        )
        database_count = Infraction.objects.all().count()
        self.assertEqual(3, database_count)

    def test_infraction_factory_multiple_users(self):
        """Does the test database hold as many infractions as we tried to create?"""
        for _user in range(5):
            InfractionFactory.create(
                actor=self.actor,
                infractions=(
                    {'type': 'kick', 'active': False, 'hidden': True},
                    {'type': 'ban', 'active': True, 'hidden': False},
                ),
                infraction_model=self.infraction_model,
                user_model=self.user_model,
            )

        # Check if infractions and users are recorded properly in the database
        database_count = Infraction.objects.all().count()
        self.assertEqual(database_count, 10)

        user_count = User.objects.all().count()
        self.assertEqual(user_count, 5 + 1)

    def test_infraction_factory_sets_correct_fields(self):
        """Does the InfractionFactory set the correct attributes?"""
        infractions = (
            {
                'type': 'note',
                'active': False,
                'hidden': True,
                'expires_at': timezone.now()
            },
            {'type': 'warning', 'active': False, 'hidden': False, 'expires_at': None},
            {'type': 'watch', 'active': False, 'hidden': True, 'expires_at': None},
            {'type': 'mute', 'active': True, 'hidden': False, 'expires_at': None},
            {'type': 'kick', 'active': True, 'hidden': True, 'expires_at': None},
            {'type': 'ban', 'active': True, 'hidden': False, 'expires_at': None},
            {
                'type': 'superstar',
                'active': True,
                'hidden': True,
                'expires_at': timezone.now()
            },
        )

        InfractionFactory.create(
            actor=self.actor,
            infractions=infractions,
            infraction_model=self.infraction_model,
            user_model=self.user_model,
        )

        for infraction in infractions:
            with self.subTest(**infraction):
                self.assertTrue(Infraction.objects.filter(**infraction).exists())


class ActiveInfractionMigrationTests(MigrationsTestCase):
    """
    Tests the active infraction data migration.

    The active infraction data migration should do the following things:

    1.  migrates all active notes, warnings, and kicks to an inactive status;
    2.  migrates all users with multiple active infractions of a single type to have only one active
        infraction of that type. The infraction with the longest duration stays active.
    """

    app = "api"
    migration_prior = "0046_reminder_jump_url"
    migration_target = "0047_active_infractions_migration"

    @classmethod
    def setUpMigrationData(cls, apps):
        """Sets up an initial database state that contains the relevant test cases."""
        # Fetch the Infraction and User model in the current migration state
        cls.infraction_model = apps.get_model('api', 'Infraction')
        cls.user_model = apps.get_model('api', 'User')

        cls.created_infractions = {}

        # Moderator that serves as actor for all infractions
        cls.user_moderator = cls.user_model.objects.create(
            id=9999,
            name="Olivier de Vienne",
            discriminator=1040,
            avatar_hash=None,
        )

        # User #1: clean user with no infractions
        cls.created_infractions["no infractions"] = InfractionFactory.create(
            actor=cls.user_moderator,
            infractions=[],
            infraction_model=cls.infraction_model,
            user_model=cls.user_model,
        )

        # User #2: One inactive note infraction
        cls.created_infractions["one inactive note"] = InfractionFactory.create(
            actor=cls.user_moderator,
            infractions=(
                {'type': 'note', 'active': False, 'hidden': True},
            ),
            infraction_model=cls.infraction_model,
            user_model=cls.user_model,
        )

        # User #3: One active note infraction
        cls.created_infractions["one active note"] = InfractionFactory.create(
            actor=cls.user_moderator,
            infractions=(
                {'type': 'note', 'active': True, 'hidden': True},
            ),
            infraction_model=cls.infraction_model,
            user_model=cls.user_model,
        )

        # User #4: One active and one inactive note infraction
        cls.created_infractions["one active and one inactive note"] = InfractionFactory.create(
            actor=cls.user_moderator,
            infractions=(
                {'type': 'note', 'active': False, 'hidden': True},
                {'type': 'note', 'active': True, 'hidden': True},
            ),
            infraction_model=cls.infraction_model,
            user_model=cls.user_model,
        )

        # User #5: Once active note, one active kick, once active warning
        cls.created_infractions["active note, kick, warning"] = InfractionFactory.create(
            actor=cls.user_moderator,
            infractions=(
                {'type': 'note', 'active': True, 'hidden': True},
                {'type': 'kick', 'active': True, 'hidden': True},
                {'type': 'warning', 'active': True, 'hidden': True},
            ),
            infraction_model=cls.infraction_model,
            user_model=cls.user_model,
        )

        # User #6: One inactive ban and one active ban
        cls.created_infractions["one inactive and one active ban"] = InfractionFactory.create(
            actor=cls.user_moderator,
            infractions=(
                {'type': 'ban', 'active': False, 'hidden': True},
                {'type': 'ban', 'active': True, 'hidden': True},
            ),
            infraction_model=cls.infraction_model,
            user_model=cls.user_model,
        )

        # User #7: Two active permanent bans
        cls.created_infractions["two active perm bans"] = InfractionFactory.create(
            actor=cls.user_moderator,
            infractions=(
                {'type': 'ban', 'active': True, 'hidden': True},
                {'type': 'ban', 'active': True, 'hidden': True},
            ),
            infraction_model=cls.infraction_model,
            user_model=cls.user_model,
        )

        # User #8: Multiple active temporary bans
        cls.created_infractions["multiple active temp bans"] = InfractionFactory.create(
            actor=cls.user_moderator,
            infractions=(
                {
                    'type': 'ban',
                    'active': True,
                    'hidden': True,
                    'expires_at': timezone.now() + timedelta(days=1)
                },
                {
                    'type': 'ban',
                    'active': True,
                    'hidden': True,
                    'expires_at': timezone.now() + timedelta(days=10)
                },
                {
                    'type': 'ban',
                    'active': True,
                    'hidden': True,
                    'expires_at': timezone.now() + timedelta(days=20)
                },
                {
                    'type': 'ban',
                    'active': True,
                    'hidden': True,
                    'expires_at': timezone.now() + timedelta(days=5)
                },
            ),
            infraction_model=cls.infraction_model,
            user_model=cls.user_model,
        )

        # User #9: One active permanent ban, two active temporary bans
        cls.created_infractions["active perm, two active temp bans"] = InfractionFactory.create(
            actor=cls.user_moderator,
            infractions=(
                {
                    'type': 'ban',
                    'active': True,
                    'hidden': True,
                    'expires_at': timezone.now() + timedelta(days=10)
                },
                {
                    'type': 'ban',
                    'active': True,
                    'hidden': True,
                    'expires_at': None,
                },
                {
                    'type': 'ban',
                    'active': True,
                    'hidden': True,
                    'expires_at': timezone.now() + timedelta(days=7)
                },
            ),
            infraction_model=cls.infraction_model,
            user_model=cls.user_model,
        )

        # User #10: One inactive permanent ban, two active temporary bans
        cls.created_infractions["one inactive perm ban, two active temp bans"] = (
            InfractionFactory.create(
                actor=cls.user_moderator,
                infractions=(
                    {
                        'type': 'ban',
                        'active': True,
                        'hidden': True,
                        'expires_at': timezone.now() + timedelta(days=10)
                    },
                    {
                        'type': 'ban',
                        'active': False,
                        'hidden': True,
                        'expires_at': None,
                    },
                    {
                        'type': 'ban',
                        'active': True,
                        'hidden': True,
                        'expires_at': timezone.now() + timedelta(days=7)
                    },
                ),
                infraction_model=cls.infraction_model,
                user_model=cls.user_model,
            )
        )

        # User #11: Active ban, active mute, active superstar
        cls.created_infractions["active ban, mute, and superstar"] = InfractionFactory.create(
            actor=cls.user_moderator,
            infractions=(
                {'type': 'ban', 'active': True, 'hidden': True},
                {'type': 'mute', 'active': True, 'hidden': True},
                {'type': 'superstar', 'active': True, 'hidden': True},
                {'type': 'watch', 'active': True, 'hidden': True},
            ),
            infraction_model=cls.infraction_model,
            user_model=cls.user_model,
        )

        # User #12: Multiple active bans, active mutes, active superstars
        cls.created_infractions["multiple active bans, mutes, stars"] = InfractionFactory.create(
            actor=cls.user_moderator,
            infractions=(
                {'type': 'ban', 'active': True, 'hidden': True},
                {'type': 'ban', 'active': True, 'hidden': True},
                {'type': 'ban', 'active': True, 'hidden': True},
                {'type': 'mute', 'active': True, 'hidden': True},
                {'type': 'mute', 'active': True, 'hidden': True},
                {'type': 'mute', 'active': True, 'hidden': True},
                {'type': 'superstar', 'active': True, 'hidden': True},
                {'type': 'superstar', 'active': True, 'hidden': True},
                {'type': 'superstar', 'active': True, 'hidden': True},
                {'type': 'watch', 'active': True, 'hidden': True},
                {'type': 'watch', 'active': True, 'hidden': True},
                {'type': 'watch', 'active': True, 'hidden': True},
            ),
            infraction_model=cls.infraction_model,
            user_model=cls.user_model,
        )

    def test_all_never_active_types_became_inactive(self):
        """Are all infractions of a non-active type inactive after the migration?"""
        inactive_type_query = Q(type="note") | Q(type="warning") | Q(type="kick")
        self.assertFalse(
            self.infraction_model.objects.filter(inactive_type_query, active=True).exists()
        )

    def test_migration_left_clean_user_without_infractions(self):
        """Do users without infractions have no infractions after the migration?"""
        user_id, infraction_history = self.created_infractions["no infractions"]
        self.assertFalse(
            self.infraction_model.objects.filter(user__id=user_id).exists()
        )

    def test_migration_left_user_with_inactive_note_untouched(self):
        """Did the migration leave users with only an inactive note untouched?"""
        user_id, infraction_history = self.created_infractions["one inactive note"]
        inactive_note = infraction_history[0]
        self.assertTrue(
            self.infraction_model.objects.filter(**model_to_dict(inactive_note)).exists()
        )

    def test_migration_only_touched_active_field_of_active_note(self):
        """Does the migration only change the `active` field?"""
        user_id, infraction_history = self.created_infractions["one active note"]
        note = model_to_dict(infraction_history[0])
        note['active'] = False
        self.assertTrue(
            self.infraction_model.objects.filter(**note).exists()
        )

    def test_migration_only_touched_active_field_of_active_note_left_inactive_untouched(self):
        """Does the migration only change the `active` field of active notes?"""
        user_id, infraction_history = self.created_infractions["one active and one inactive note"]
        for note in infraction_history:
            with self.subTest(active=note.active):
                note = model_to_dict(note)
                note['active'] = False
                self.assertTrue(
                    self.infraction_model.objects.filter(**note).exists()
                )

    def test_migration_migrates_all_nonactive_types_to_inactive(self):
        """Do we set the `active` field of all non-active infractions to `False`?"""
        user_id, infraction_history = self.created_infractions["active note, kick, warning"]
        self.assertFalse(
            self.infraction_model.objects.filter(user__id=user_id, active=True).exists()
        )

    def test_migration_leaves_user_with_one_active_ban_untouched(self):
        """Do we leave a user with one active and one inactive ban untouched?"""
        user_id, infraction_history = self.created_infractions["one inactive and one active ban"]
        for infraction in infraction_history:
            with self.subTest(active=infraction.active):
                self.assertTrue(
                    self.infraction_model.objects.filter(**model_to_dict(infraction)).exists()
                )

    def test_migration_turns_double_active_perm_ban_into_single_active_perm_ban(self):
        """Does the migration turn two active permanent bans into one active permanent ban?"""
        user_id, infraction_history = self.created_infractions["two active perm bans"]
        active_count = self.infraction_model.objects.filter(user__id=user_id, active=True).count()
        self.assertEqual(active_count, 1)

    def test_migration_leaves_temporary_ban_with_longest_duration_active(self):
        """Does the migration turn two active permanent bans into one active permanent ban?"""
        user_id, infraction_history = self.created_infractions["multiple active temp bans"]
        active_ban = self.infraction_model.objects.get(user__id=user_id, active=True)
        self.assertEqual(active_ban.expires_at, infraction_history[2].expires_at)

    def test_migration_leaves_permanent_ban_active(self):
        """Does the migration leave the permanent ban active?"""
        user_id, infraction_history = self.created_infractions["active perm, two active temp bans"]
        active_ban = self.infraction_model.objects.get(user__id=user_id, active=True)
        self.assertIsNone(active_ban.expires_at)

    def test_migration_leaves_longest_temp_ban_active_with_inactive_permanent_ban(self):
        """Does the longest temp ban stay active, even with an inactive perm ban present?"""
        user_id, infraction_history = self.created_infractions[
            "one inactive perm ban, two active temp bans"
        ]
        active_ban = self.infraction_model.objects.get(user__id=user_id, active=True)
        self.assertEqual(active_ban.expires_at, infraction_history[0].expires_at)

    def test_migration_leaves_all_active_types_active_if_one_of_each_exists(self):
        """Do all active infractions stay active if only one of each is present?"""
        user_id, infraction_history = self.created_infractions["active ban, mute, and superstar"]
        active_count = self.infraction_model.objects.filter(user__id=user_id, active=True).count()
        self.assertEqual(active_count, 4)

    def test_migration_reduces_all_active_types_to_a_single_active_infraction(self):
        """Do we reduce all of the infraction types to one active infraction?"""
        user_id, infraction_history = self.created_infractions["multiple active bans, mutes, stars"]
        active_infractions = self.infraction_model.objects.filter(user__id=user_id, active=True)
        self.assertEqual(len(active_infractions), 4)
        types_observed = [infraction.type for infraction in active_infractions]

        for infraction_type in ('ban', 'mute', 'superstar', 'watch'):
            with self.subTest(type=infraction_type):
                self.assertIn(infraction_type, types_observed)
