"""Includes utilities for testing migrations."""
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase


class MigrationsTestCase(TestCase):
    """
    A `TestCase` subclass to test migration files.

    To be able to properly test a migration, we will need to inject data into the test database
    before the migrations we want to test are applied, but after the older migrations have been
    applied. This makes sure that we are testing "as if" we were actually applying this migration
    to a database in the state it was in before introducing the new migration.

    To set up a MigrationsTestCase, create a subclass of this class and set the following
    class-level attributes:

    - app: The name of the app that contains the migrations (e.g., `'api'`)
    - migration_prior: The name* of the last migration file before the migrations you want to test
    - migration_target: The name* of the last migration file we want to test

    *) Specify the file names without a path or the `.py` file extension.

    Additionally, overwrite the `setUpMigrationData` in the subclass to inject data into the
    database before the migrations we want to test are applied. Please read the docstring of the
    method for more information. An optional hook, `setUpPostMigrationData` is also provided.
    """

    # These class-level attributes should be set in classes that inherit from this base class.
    app = None
    migration_prior = None
    migration_target = None

    @classmethod
    def setUpTestData(cls):
        """
        Injects data into the test database prior to the migration we're trying to test.

        This class methods reverts the test database back to the state of the last migration file
        prior to the migrations we want to test. It will then allow the user to inject data into the
        test database by calling the `setUpMigrationData` hook. After the data has been injected, it
        will apply the migrations we want to test and call the `setUpPostMigrationData` hook. The
        user can now test if the migration correctly migrated the injected test data.
        """
        if not cls.app:
            raise ValueError("The `app` attribute was not set.")

        if not cls.migration_prior or not cls.migration_target:
            raise ValueError("Both ` migration_prior` and `migration_target` need to be set.")

        cls.migrate_from = [(cls.app, cls.migration_prior)]
        cls.migrate_to = [(cls.app, cls.migration_target)]

        # Reverse to database state prior to the migrations we want to test
        executor = MigrationExecutor(connection)
        executor.migrate(cls.migrate_from)

        # Call the data injection hook with the current state of the project
        old_apps = executor.loader.project_state(cls.migrate_from).apps
        cls.setUpMigrationData(old_apps)

        # Run the migrations we want to test
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        executor.migrate(cls.migrate_to)

        # Save the project state so we're able to work with the correct model states
        cls.apps = executor.loader.project_state(cls.migrate_to).apps

        # Call `setUpPostMigrationData` to potentially set up post migration data used in testing
        cls.setUpPostMigrationData(cls.apps)

    @classmethod
    def setUpMigrationData(cls, apps):
        """
        Override this method to inject data into the test database before the migration is applied.

        This method will be called after setting up the database according to the migrations that
        come before the migration(s) we are trying to test, but before the to-be-tested migration(s)
        are applied. This allows us to simulate a database state just prior to the migrations we are
        trying to test.

        To make sure we're creating objects according to the state the models were in at this point
        in the migration history, use `apps.get_model(app_name: str, model_name: str)` to get the
        appropriate model, e.g.:

        >>> Infraction = apps.get_model('api', 'Infraction')
        """
        pass

    @classmethod
    def setUpPostMigrationData(cls, apps):
        """
        Set up additional test data after the target migration has been applied.

        Use `apps.get_model(app_name: str, model_name: str)` to get the correct instances of the
        model classes:

        >>> Infraction = apps.get_model('api', 'Infraction')
        """
        pass
