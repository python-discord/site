import os

from flask import Blueprint
from flask_testing import TestCase

os.environ["BOT_API_KEY"] = "abcdefg"  # This is a constant, must be done first
os.environ["PAPERTRAIL_ADDRESS"] = 'localhost'  # satisfies coverage
os.environ["DATADOG_ADDRESS"] = 'localhost'  # satisfies coverage

if "FLASK_DEBUG" in os.environ:
    del os.environ["FLASK_DEBUG"]  # Some unit tests fail if this is set

from app import manager
from gunicorn_config import _when_ready as when_ready

when_ready()

manager.app.tests_blueprint = Blueprint("tests", __name__)
manager.load_views(manager.app.tests_blueprint, "pysite/views/tests")
manager.app.register_blueprint(manager.app.tests_blueprint)
app = manager.app

app.config["WTF_CSRF_CHECK_DEFAULT"] = False


class SiteTest(TestCase):
    """ Extend TestCase with flask app instantiation """

    def create_app(self):
        """ Add flask app configuration settings """
        server_name = 'pytest.local'

        app.config['TESTING'] = True
        app.config['LIVESERVER_TIMEOUT'] = 10
        app.config['SERVER_NAME'] = server_name
        app.config['API_SUBDOMAIN'] = f'http://api.{server_name}'
        app.config['STAFF_SUBDOMAIN'] = f'http://staff.{server_name}'
        app.config['WIKI_SUBDOMAIN'] = f'http://wiki.{server_name}'
        app.config['TEST_HEADER'] = {'X-API-Key': 'abcdefg', 'Content-Type': 'application/json'}
        app.allow_subdomain_redirects = True

        return app
