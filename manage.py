#!/usr/bin/env python
import os
import platform
import sys
import warnings
from pathlib import Path

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
    Manages the preparation and serving of the website for local use.

    This class is used solely for setting up the development
    environment. In production, gunicorn is invoked directly
    and migrations are handled in an init container.

    Usage:
        manage.py run [option]...

    Options:
        --silent   Sets minimal console output.
        --verbose  Sets verbose console output.
    """

    def __init__(self, args: list[str]):
        self.silent = "--silent" in args

        if self.silent:
            self.verbosity = 0
        else:
            self.verbosity = 2 if "--verbose" in args else 1

        os.environ.setdefault("DEBUG", "true")
        print("Starting in debug mode.")

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

    def prepare_environment(self) -> None:
        """Perform common preparation tasks."""
        django.setup()

        print("Applying migrations.")
        call_command("migrate", verbosity=self.verbosity)

    def prepare_server(self) -> None:
        """Perform debug runserver-specific preparation tasks."""
        print("Collecting static files.")
        call_command(
            "collectstatic",
            interactive=False,
            clear=True,
            verbosity=self.verbosity - 1
        )

        self.set_dev_site_name()
        self.create_superuser()

    def run_debug(self) -> None:
        """Prepare and run the debug web server."""
        in_reloader = os.environ.get('RUN_MAIN') == 'true'

        # Prevent preparing twice when in dev mode due to reloader
        if in_reloader:
            self.prepare_environment()
            self.prepare_server()

        print("Starting server.")

        # Run the development server
        call_command("runserver", "0.0.0.0:8000")

    def run_tests(self) -> None:
        """Prepare and run the test suite."""
        self.prepare_environment()
        # The whitenoise package expects a staticfiles directory to exist during startup,
        # else it raises a warning. This is fine under normal application, but during
        # tests, staticfiles are not, and do not need to be generated.
        # The following line suppresses the warning.
        # Reference: https://github.com/evansd/whitenoise/issues/215
        warnings.filterwarnings(
            action='ignore',
            category=UserWarning,
            message=r"^No directory at: .*staticfiles/$"
        )
        call_command(*sys.argv[1:])


def clean_up_static_files(build_folder: Path) -> None:
    """Recursively loop over the build directory and fix links."""
    for file in build_folder.iterdir():
        if file.is_dir():
            clean_up_static_files(file)
        elif file.name.endswith(".html"):
            # Fix parent host url
            new = file.read_text(encoding="utf-8").replace(f"//{os.getenv('PARENT_HOST')}", "")

            # Fix windows paths if on windows
            if platform.system() == "Windows":
                new = new.replace("%5C", "/")

            file.write_text(new, encoding="utf-8")


def main() -> None:
    """Entry point for Django management script."""
    # Use the custom site manager for launching the server
    if len(sys.argv) > 1 and sys.argv[1] in ("run", "test"):
        manager = SiteManager(sys.argv)
        if sys.argv[1] == "run":
            manager.run_debug()
        elif sys.argv[1] == "test":
            manager.run_tests()

    # Pass any others directly to standard management commands
    else:
        _static_build = len(sys.argv) > 1 and "distill" in sys.argv[1]

        if _static_build:
            # Build a static version of the site with no databases and API support
            os.environ["STATIC_BUILD"] = "True"
            if not os.getenv("PARENT_HOST"):
                os.environ["PARENT_HOST"] = "REPLACE_THIS.HOST"

        execute_from_command_line(sys.argv)

        if _static_build:
            # Clean up parent host in generated files
            for arg in sys.argv[2:]:
                if not arg.startswith("-"):
                    clean_up_static_files(Path(arg))
                    break


if __name__ == '__main__':
    main()
