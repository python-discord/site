#!/usr/bin/env python
import os
import socket
import sys
import time
from urllib.parse import SplitResult, urlsplit

import django
from django.contrib.auth import get_user_model
from django.core.management import call_command, execute_from_command_line

DEFAULT_ENVS = {
    "DJANGO_SETTINGS_MODULE": "pydis_site.settings",
    "SUPER_USERNAME": "admin",
    "SUPER_PASSWORD": "admin",
    "DEFAULT_BOT_API_KEY": "badbot13m0n8f570f942013fc818f234916ca531",
}

try:
    import dotenv
    dotenv.load_dotenv()
except ModuleNotFoundError:
    pass

for key, value in DEFAULT_ENVS.items():
    os.environ.setdefault(key, value)


class SiteManager:
    """
    Manages the preparation and serving of the website.

    Handles both development and production environments.

    Usage:
        manage.py run [option]...

    Options:
        --debug    Runs a development server with debug mode enabled.
        --silent   Sets minimal console output.
        --verbose  Sets verbose console output.
    """

    def __init__(self, args: list[str]):
        self.debug = "--debug" in args
        self.silent = "--silent" in args

        if self.silent:
            self.verbosity = 0
        else:
            self.verbosity = 2 if "--verbose" in args else 1

        if self.debug:
            os.environ.setdefault("DEBUG", "true")
            print("Starting in debug mode.")

    @staticmethod
    def parse_db_url(db_url: str) -> SplitResult:
        """Validate and split the given databse url."""
        db_url_parts = urlsplit(db_url)
        if not all((
            db_url_parts.hostname,
            db_url_parts.username,
            db_url_parts.password,
            db_url_parts.path
        )):
            raise ValueError(
                "The DATABASE_URL environment variable is not a valid PostgreSQL database URL."
            )
        return db_url_parts

    @staticmethod
    def create_superuser() -> None:
        """Create a default django admin super user in development environments."""
        print("Creating a superuser.")

        name = os.environ["SUPER_USERNAME"]
        password = os.environ["SUPER_PASSWORD"]
        bot_token = os.environ["DEFAULT_BOT_API_KEY"]
        user = get_user_model()

        # Get or create admin superuser.
        if user.objects.filter(username=name).exists():
            user = user.objects.get(username=name)
            print('Admin superuser already exists.')
        else:
            user = user.objects.create_superuser(name, '', password)
            print('Admin superuser created.')

        # Setup a default bot token to connect with site API
        from rest_framework.authtoken.models import Token
        token, is_new = Token.objects.update_or_create(user=user)
        if token.key != bot_token:
            token.delete()
        token, is_new = Token.objects.update_or_create(user=user, key=bot_token)
        if is_new:
            print(f"New bot token created: {token}")
        else:
            print(f"Existing bot token found: {token}")

    @staticmethod
    def wait_for_postgres() -> None:
        """Wait for the PostgreSQL database specified in DATABASE_URL."""
        print("Waiting for PostgreSQL database.")

        # Get database URL based on environmental variable passed in compose
        database_url_parts = SiteManager.parse_db_url(os.environ["DATABASE_URL"])
        domain = database_url_parts.hostname
        # Port may be omitted, 5432 is the default psql port
        port = database_url_parts.port or 5432

        # Attempt to connect to the database socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        attempts_left = 10
        while attempts_left:
            try:
                # Ignore 'incomplete startup packet'
                s.connect((domain, port))
                s.shutdown(socket.SHUT_RDWR)
                print("Database is ready.")
                break
            except socket.error:
                attempts_left -= 1
                print("Not ready yet, retrying.")
                time.sleep(0.5)
        else:
            print("Database could not be found, exiting.")
            sys.exit(1)

    @staticmethod
    def set_dev_site_name() -> None:
        """Set the development site domain in admin from default example."""
        # import Site model now after django setup
        from django.contrib.sites.models import Site
        query = Site.objects.filter(id=1)
        site = query.get()
        if site.domain == "example.com":
            query.update(
                domain="pythondiscord.local:8000",
                name="pythondiscord.local:8000"
            )

    @staticmethod
    def run_metricity_init() -> None:
        """
        Initialise metricity relations and populate with some testing data.

        This is done at run time since other projects, like Python bot,
        rely on the site initialising it's own db, since they do not have
        access to the init.sql file to mount a docker-compose volume.
        """
        import psycopg2
        from psycopg2 import sql
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

        print("Initialising metricity.")

        site_db_url_parts = SiteManager.parse_db_url(os.environ["DATABASE_URL"])
        metricity_db_url_parts = SiteManager.parse_db_url(os.environ["METRICITY_DB_URL"])

        conn = psycopg2.connect(
            host=site_db_url_parts.hostname,
            port=site_db_url_parts.port,
            user=site_db_url_parts.username,
            password=site_db_url_parts.password,
            database=site_db_url_parts.path[1:]
        )
        # Required to create a db from `cursor.execute()`
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        metricity_db_name = metricity_db_url_parts.path[1:]
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
                (metricity_db_name,)
            )
            if cursor.fetchone():
                print("Metricity already exists.")
                return

            cursor.execute(
                sql.SQL("CREATE DATABASE {db}").format(
                    db=sql.Identifier(metricity_db_name)
                )
            )
        conn.close()

        # PostgreSQL can't switch database contexts without switching connection.
        # dblink extension could work, but we'd need to wrap every statement with dblink_exec()
        conn = psycopg2.connect(
            host=metricity_db_url_parts.hostname,
            port=metricity_db_url_parts.port,
            user=metricity_db_url_parts.username,
            password=metricity_db_url_parts.password,
            database=metricity_db_url_parts.path[1:]
        )
        conn.autocommit = True
        with conn.cursor() as cursor, open("postgres/init.sql", encoding="utf-8") as f:
            cursor.execute(f.read())
        conn.close()

    def prepare_server(self) -> None:
        """Perform preparation tasks before running the server."""
        self.wait_for_postgres()
        if self.debug:
            self.run_metricity_init()

        django.setup()

        print("Applying migrations.")
        call_command("migrate", verbosity=self.verbosity)

        if self.debug:
            # In Production, collectstatic is ran in the Docker image
            print("Collecting static files.")
            call_command(
                "collectstatic",
                interactive=False,
                clear=True,
                verbosity=self.verbosity - 1
            )

            self.set_dev_site_name()
            self.create_superuser()

    def run_server(self) -> None:
        """Prepare and run the web server."""
        in_reloader = os.environ.get('RUN_MAIN') == 'true'

        # Prevent preparing twice when in dev mode due to reloader
        if not self.debug or in_reloader:
            self.prepare_server()

        print("Starting server.")

        # Run the development server
        if self.debug:
            call_command("runserver", "0.0.0.0:8000")
            return

        # Import gunicorn only if we aren't in debug mode.
        import gunicorn.app.wsgiapp

        # Patch the arguments for gunicorn
        sys.argv = [
            "gunicorn",
            "--preload",
            "-b", "0.0.0.0:8000",
            "pydis_site.wsgi:application",
            "-w", "2",
            "--statsd-host", "graphite.default.svc.cluster.local:8125",
            "--statsd-prefix", "site",
            "--config", "file:gunicorn.conf.py"
        ]

        # Run gunicorn for the production server.
        gunicorn.app.wsgiapp.run()


def main() -> None:
    """Entry point for Django management script."""
    # Always run metricity init when in CI, indicated by the CI env var
    if os.environ.get("CI", "false").lower() == "true":
        SiteManager.wait_for_postgres()
        SiteManager.run_metricity_init()

    # Use the custom site manager for launching the server
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        SiteManager(sys.argv).run_server()

    # Pass any others directly to standard management commands
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
