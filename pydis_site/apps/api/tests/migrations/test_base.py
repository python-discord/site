import logging
from unittest.mock import call, patch

from django.db.migrations.loader import MigrationLoader
from django.test import TestCase

from .base import MigrationsTestCase, connection

log = logging.getLogger(__name__)


class SpanishInquisition(MigrationsTestCase):
    app = "api"
    migration_prior = "scragly"
    migration_target = "kosa"


@patch("pydis_site.apps.api.tests.migrations.base.MigrationExecutor")
class MigrationsTestCaseNoSideEffectsTests(TestCase):
    """Tests the MigrationTestCase class with actual migration side effects disabled."""

    def setUp(self):
        """Set up an instance of MigrationsTestCase for use in tests."""
        self.test_case = SpanishInquisition()

    def test_missing_app_class_raises_value_error(self, _migration_executor):
        """A MigrationsTestCase subclass should set the class-attribute `app`."""
        class Spam(MigrationsTestCase):
            pass

        spam = Spam()
        with self.assertRaises(ValueError, msg="The `app` attribute was not set."):
            spam.setUpTestData()

    def test_missing_migration_class_attributes_raise_value_error(self, _migration_executor):
        """A MigrationsTestCase subclass should set both `migration_prior` and `migration_target`"""
        class Eggs(MigrationsTestCase):
            app = "api"
            migration_target = "lemon"

        class Bacon(MigrationsTestCase):
            app = "api"
            migration_prior = "mark"

        instances = (Eggs(), Bacon())

        exception_message = "Both ` migration_prior` and `migration_target` need to be set."
        for instance in instances:
            with self.subTest(
                    migration_prior=instance.migration_prior,
                    migration_target=instance.migration_target,
            ):
                with self.assertRaises(ValueError, msg=exception_message):
                    instance.setUpTestData()

    @patch(f"{__name__}.SpanishInquisition.setUpMigrationData")
    @patch(f"{__name__}.SpanishInquisition.setUpPostMigrationData")
    def test_migration_data_hooks_are_called_once(self, pre_hook, post_hook, _migration_executor):
        """The `setUpMigrationData` and `setUpPostMigrationData` hooks should be called once."""
        self.test_case.setUpTestData()
        for hook in (pre_hook, post_hook):
            with self.subTest(hook=repr(hook)):
                hook.assert_called_once()

    def test_migration_executor_is_instantiated_twice(self, migration_executor):
        """The `MigrationExecutor` should be instantiated with the database connection twice."""
        self.test_case.setUpTestData()

        expected_args = [call(connection), call(connection)]
        self.assertEqual(migration_executor.call_args_list, expected_args)

    def test_project_state_is_loaded_for_correct_migration_files_twice(self, migration_executor):
        """The `project_state` should first be loaded with `migrate_from`, then `migrate_to`."""
        self.test_case.setUpTestData()

        expected_args = [call(self.test_case.migrate_from), call(self.test_case.migrate_to)]
        self.assertEqual(migration_executor().loader.project_state.call_args_list, expected_args)

    def test_loader_build_graph_gets_called_once(self, migration_executor):
        """We should rebuild the migration graph before applying the second set of migrations."""
        self.test_case.setUpTestData()

        migration_executor().loader.build_graph.assert_called_once()

    def test_migration_executor_migrate_method_is_called_correctly_twice(self, migration_executor):
        """The migrate method of the executor should be called twice with the correct arguments."""
        self.test_case.setUpTestData()

        self.assertEqual(migration_executor().migrate.call_count, 2)
        calls = [call([('api', 'scragly')]), call([('api', 'kosa')])]
        migration_executor().migrate.assert_has_calls(calls)


class LifeOfBrian(MigrationsTestCase):
    app = "api"
    migration_prior = "0046_reminder_jump_url"
    migration_target = "0048_add_infractions_unique_constraints_active"

    @classmethod
    def log_last_migration(cls):
        """Parses the applied migrations dictionary to log the last applied migration."""
        loader = MigrationLoader(connection)
        api_migrations = [
            migration for app, migration in loader.applied_migrations if app == cls.app
        ]
        last_migration = max(api_migrations, key=lambda name: int(name[:4]))
        log.info(f"The last applied migration: {last_migration}")

    @classmethod
    def setUpMigrationData(cls, apps):
        """Method that logs the last applied migration at this point."""
        cls.log_last_migration()

    @classmethod
    def setUpPostMigrationData(cls, apps):
        """Method that logs the last applied migration at this point."""
        cls.log_last_migration()


class MigrationsTestCaseMigrationTest(TestCase):
    """Tests if `MigrationsTestCase` travels to the right points in the migration history."""

    def test_migrations_test_case_travels_to_correct_migrations_in_history(self):
        """The test case should first revert to `migration_prior`, then go to `migration_target`."""
        brian = LifeOfBrian()

        with self.assertLogs(log, level=logging.INFO) as logs:
            brian.setUpTestData()

            self.assertEqual(len(logs.records), 2)

            for time_point, record in zip(("migration_prior", "migration_target"), logs.records):
                with self.subTest(time_point=time_point):
                    message = f"The last applied migration: {getattr(brian, time_point)}"
                    self.assertEqual(record.getMessage(), message)
