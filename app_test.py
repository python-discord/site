
import json
import os

from flask import Blueprint
from flask_testing import TestCase

os.environ["BOT_API_KEY"] = "abcdefg"  # This is a constant, must be done first
try:
    del os.environ["FLASK_DEBUG"]  # Some unit tests fail if this is set
except KeyError:
    pass

from app import manager
from gunicorn_config import _when_ready as when_ready

from pysite.constants import DISCORD_OAUTH_REDIRECT, DISCORD_OAUTH_AUTHORIZED

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
        app.allow_subdomain_redirects = True

        return app


class RootEndpoint(SiteTest):
    """ Test cases for the root endpoint and error handling """

    def test_index(self):
        """ Check the root path responds with 200 OK """
        response = self.client.get('/', 'http://pytest.local')
        self.assertEqual(response.status_code, 200)

    def test_info_index(self):
        """ Check the info index path responds with a 301 """
        response = self.client.get('/info')
        self.assertEqual(response.status_code, 301)

    def test_info_help(self):
        """ Check the info help path responds with 200 OK """
        response = self.client.get('/info/help')
        self.assertEqual(response.status_code, 200)

    def test_info_resources(self):
        """ Check the info resources path responds with 200 OK """
        response = self.client.get('/info/resources')
        self.assertEqual(response.status_code, 200)

    def test_info_resources_json(self):
        """ Check the resources JSON loads correctly """
        response = self.client.get('/static/resources.json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), dict)

    def test_info_rules(self):
        """ Check the info rules path responds with 200 OK """
        response = self.client.get('/info/help')
        self.assertEqual(response.status_code, 200)

    def test_not_found(self):
        """ Check paths without handlers returns 404 Not Found """
        response = self.client.get('/nonexistentpath')
        self.assertEqual(response.status_code, 404)

    def test_error(self):
        """ Check the /error/XYZ page """
        response = self.client.get('/error/418')
        self.assertEqual(response.status_code, 418)

    def test_invite(self):
        """ Check invite redirects """
        response = self.client.get('/invite')
        self.assertEqual(response.status_code, 302)

    def test_ws_test(self):
        """ Check ws_test responds """
        response = self.client.get('/ws_test')
        self.assertEqual(response.status_code, 200)

    def test_oauth_redirects(self):
        """ Check oauth redirects """
        response = self.client.get(DISCORD_OAUTH_REDIRECT)
        self.assertEqual(response.status_code, 302)

    def test_oauth_logout(self):
        """ Check oauth redirects """
        response = self.client.get('/auth/logout')
        self.assertEqual(response.status_code, 302)

    def test_oauth_authorized(self):
        """ Check oauth authorization """
        response = self.client.get(DISCORD_OAUTH_AUTHORIZED)
        self.assertEqual(response.status_code, 302)

    def test_stats_redirect(self):
        """ Check stats path redirects """
        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 302)

    def test_500_easter_egg(self):
        """ Check the status of the /500 page"""
        response = self.client.get("/500")
        self.assertEqual(response.status_code, 500)


class WikiEndpoints(SiteTest):
    """ Test cases for the wiki subdomain """
    def test_wiki_edit(self):
        """Test that the wiki edit page redirects to login"""
        response = self.client.get("/edit/page", app.config['WIKI_SUBDOMAIN'])
        self.assertEqual(response.status_code, 302)

    def test_wiki_edit_post_empty_request(self):
        """Empty request should redirect to login"""
        response = self.client.post("/edit/page", app.config['WIKI_SUBDOMAIN'])
        self.assertEqual(response.status_code, 302)

    def test_wiki_history(self):
        """Test the history show"""
        response = self.client.get("/history/show/blahblah-non-existant-page", app.config['WIKI_SUBDOMAIN'])
        self.assertEqual(response.status_code, 404) # Test that unknown routes 404

    def test_wiki_diff(self):
        """Test whether invalid revision IDs error"""
        response = self.client.get("/history/compare/ABC/XYZ", app.config['WIKI_SUBDOMAIN'])
        self.assertEqual(response.status_code, 404) # Test that unknown revisions 404


class ApiEndpoints(SiteTest):
    """ Test cases for the api subdomain """
    def test_api_unknown_route(self):
        """ Check api unknown route """
        response = self.client.get('/', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.json, {'error_code': 0, 'error_message': 'Unknown API route'})
        self.assertEqual(response.status_code, 404)

    def test_api_healthcheck(self):
        """ Check healthcheck url responds """
        response = self.client.get('/healthcheck', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.json, {'status': 'ok'})
        self.assertEqual(response.status_code, 200)

    def test_snake_endpoints(self):
        """
        Tests the following endpoints:
            - snake_movies
            - snake_quiz
            - snake_names
            - snake_idioms
            - snake_facts
        """

        os.environ['BOT_API_KEY'] = 'abcdefg'
        headers = {'X-API-Key': 'abcdefg', 'Content-Type': 'application/json'}

        # GET method - get snake fact
        response = self.client.get('/snake_facts', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), str)

        # GET method - get snake idiom
        response = self.client.get('/snake_idioms', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), str)

        # GET method - get snake quiz
        response = self.client.get('/snake_quiz', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), dict)

        # GET method - get snake name
        response = self.client.get('/snake_names', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), dict)

        # GET method - get all snake names
        response = self.client.get('/snake_names?get_all=True', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), list)

    def test_api_tags(self):
        """ Check tag API """
        os.environ['BOT_API_KEY'] = 'abcdefg'
        headers = {'X-API-Key': 'abcdefg', 'Content-Type': 'application/json'}

        post_data = json.dumps({
            'tag_name': 'testing',
            'tag_content': 'testing'
        })

        get_data = json.dumps({
            'tag_name': 'testing'
        })

        bad_data = json.dumps({
            'not_a_valid_key': 'gross_faceman'
        })

        # POST method - no headers
        response = self.client.post('/tags', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.status_code, 401)

        # POST method - no data
        response = self.client.post('/tags', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.status_code, 400)

        # POST method - bad data
        response = self.client.post('/tags', app.config['API_SUBDOMAIN'], headers=headers, data=bad_data)
        self.assertEqual(response.status_code, 400)

        # POST method - save tag
        response = self.client.post('/tags', app.config['API_SUBDOMAIN'], headers=headers, data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True})

        # GET method - no headers
        response = self.client.get('/tags', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.status_code, 401)

        # GET method - get all tags
        response = self.client.get('/tags', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), list)

        # GET method - get specific tag
        response = self.client.get('/tags?tag_name=testing', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.json, {
            'tag_content': 'testing',
            'tag_name': 'testing'
        })
        self.assertEqual(response.status_code, 200)

        # DELETE method - no headers
        response = self.client.delete('/tags', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.status_code, 401)

        # DELETE method - no data
        response = self.client.delete('/tags', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.status_code, 400)

        # DELETE method - bad data
        response = self.client.delete('/tags', app.config['API_SUBDOMAIN'], headers=headers, data=bad_data)
        self.assertEqual(response.status_code, 400)

        # DELETE method - delete the testing tag
        response = self.client.delete('/tags', app.config['API_SUBDOMAIN'], headers=headers, data=get_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True})

    def test_api_user(self):
        """ Check insert user """

        os.environ['BOT_API_KEY'] = 'abcdefg'
        headers = {'X-API-Key': 'abcdefg', 'Content-Type': 'application/json'}
        single_data = json.dumps({'user_id': "1234", 'roles': ["5678"], "username": "test", "discriminator": "0000"})
        list_data = json.dumps([{'user_id': "1234", 'roles': ["5678"], "username": "test", "discriminator": "0000"}])

        response = self.client.get('/user', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.status_code, 405)

        response = self.client.post('/user', app.config['API_SUBDOMAIN'], headers=headers, data=single_data)
        self.assertTrue("inserted" in response.json)

        response = self.client.post('/user', app.config['API_SUBDOMAIN'], headers=headers, data=list_data)
        self.assertTrue("inserted" in response.json)

    def test_api_route_errors(self):
        """ Check api route errors """
        from pysite.base_route import APIView
        from pysite.constants import ErrorCodes

        av = APIView()
        av.error(ErrorCodes.unauthorized)
        av.error(ErrorCodes.bad_data_format)

    def test_not_found(self):
        """ Check paths without handlers returns 404 Not Found """
        response = self.client.get('/nonexistentpath')
        self.assertEqual(response.status_code, 404)


class StaffEndpoints(SiteTest):
    """ Test cases for staff subdomain """
    def test_staff_view(self):
        """ Check staff view redirects """
        response = self.client.get('/', app.config['STAFF_SUBDOMAIN'])
        self.assertEqual(response.status_code, 302)


class Utilities(SiteTest):
    """ Test cases for internal utility code """
    def test_error_view_runtime_error(self):
        """ Check that wrong values for error view setup raises runtime error """
        import pysite.base_route

        ev = pysite.base_route.ErrorView()
        try:
            ev.setup(manager, 'sdfsdf')
        except RuntimeError:
            return True
        raise Exception('Expected runtime error on setup() when giving wrongful arguments')

    def test_websocket_callback(self):
        """ Check that websocket default callbacks work """
        import pysite.websockets

        class TestWS(pysite.websockets.WS):
            pass

        try:
            TestWS(None).on_message("test")
            return False
        except NotImplementedError:
            return True


class MixinTests(SiteTest):
    """ Test cases for mixins """

    def test_handler_5xx(self):
        """ Check error view returns error message """
        from werkzeug.exceptions import InternalServerError
        from pysite.views.error_handlers import http_5xx

        error_view = http_5xx.Error500View()
        error_message = error_view.get(InternalServerError)
        self.assertEqual(error_message[1], 500)

    def test_route_view_runtime_error(self):
        """ Check that wrong values for route view setup raises runtime error """
        from pysite.base_route import RouteView

        rv = RouteView()
        try:
            rv.setup(manager, 'sdfsdf')
        except RuntimeError:
            return True
        raise Exception('Expected runtime error on setup() when giving wrongful arguments')

    def test_route_manager(self):
        """ Check route manager """
        from pysite.route_manager import RouteManager

        os.environ['WEBPAGE_SECRET_KEY'] = 'super_secret'
        rm = RouteManager()
        self.assertEqual(rm.app.secret_key, 'super_secret')

    def test_oauth_property(self):
        """ Make sure the oauth property works"""
        from flask import Blueprint

        from pysite.route_manager import RouteView
        from pysite.oauth import OauthBackend

        class TestRoute(RouteView):
            name = "test"
            path = "/test"

        tr = TestRoute()
        tr.setup(manager, Blueprint("test", "test_name"))
        self.assertIsInstance(tr.oauth, OauthBackend)

    def test_user_data_property(self):
        """ Make sure the user_data property works"""
        from flask import Blueprint

        from pysite.route_manager import RouteView

        class TestRoute(RouteView):
            name = "test"
            path = "/test"

        tr = TestRoute()
        tr.setup(manager, Blueprint("test", "test_name"))
        self.assertIs(tr.user_data, None)

    def test_logged_in_property(self):
        """ Make sure the user_data property works"""
        from flask import Blueprint

        from pysite.route_manager import RouteView

        class TestRoute(RouteView):
            name = "test"
            path = "/test"

        tr = TestRoute()
        tr.setup(manager, Blueprint("test", "test_name"))
        self.assertIs(tr.logged_in, False)


class DecoratorTests(SiteTest):
    def test_decorator_api_json(self):
        """ Check the json validation decorator """
        from pysite.decorators import api_params
        from pysite.constants import ValidationTypes
        from schema import Schema

        SCHEMA = Schema([{"user_id": int, "role": int}])

        @api_params(schema=SCHEMA, validation_type=ValidationTypes.json)
        def try_json_type(data):
            return data

        try:
            try_json_type("not json")
        except Exception as error_message:
            self.assertEqual(type(error_message), AttributeError)

    def test_decorator_params(self):
        """ Check the params validation decorator """

        response = self.client.post('/testparams?test=params')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{'test': 'params'}])


class DatabaseTests(SiteTest):
    """ Test cases for the database module """
    def test_table_actions(self):
        import string
        import secrets
        from pysite.database import RethinkDB

        alphabet = string.ascii_letters
        generated_table_name = ''.join(secrets.choice(alphabet) for i in range(8))

        rdb = RethinkDB()
        # Create table name and expect it to work
        result = rdb.create_table(generated_table_name)
        self.assertEqual(result, True)

        # Create the same table name and expect it to already exist
        result = rdb.create_table(generated_table_name)
        self.assertEqual(result, False)

        # Drop table and expect it to work
        result = rdb.drop_table(generated_table_name)
        self.assertEqual(result, True)

        # Drop the same table and expect it to already be gone
        result = rdb.drop_table(generated_table_name)
        self.assertEqual(result, False)

        # This is to get some more code coverage
        self.assertEqual(rdb.teardown_request('_'), None)


class TestWebsocketEcho(SiteTest):
    """ Test cases for the echo endpoint """
    def testEcho(self):
        """ Check rudimentary websockets handlers work """
        from geventwebsocket.websocket import WebSocket
        from pysite.views.ws.echo import EchoWebsocket
        ew = EchoWebsocket(WebSocket)
        ew.on_open()
        ew.on_message('message')
        ew.on_close()


class TestOauthBackend(SiteTest):
    """ Test cases for the oauth.py file """

    def test_get(self):
        """ Make sure the get function returns nothing """
        self.assertIs(manager.oauth_backend.get(), None)

    def test_delete(self):
        """ Make sure the delete function returns nothing """
        self.assertIs(manager.oauth_backend.delete(None), None)

    def test_logout(self):
        """ Make sure at least apart of logout is working :/ """
        self.assertIs(manager.oauth_backend.logout(), None)

    def test_add_user(self):
        """ Make sure function adds values to database and session """
        from flask import session

        from pysite.constants import OAUTH_DATABASE

        sess_id = "hey bro wazup"
        fake_token = {"access_token": "access_token", "id": sess_id, "refresh_token": "refresh_token", "expires_at": 5}
        fake_user = {"id": 1235678987654321, "username": "Zwacky", "discriminator": "#6660", "email": "z@g.co"}
        manager.db.conn = manager.db.get_connection()
        manager.oauth_backend.add_user(fake_token, fake_user, sess_id)

        self.assertEqual(sess_id, session["session_id"])
        fake_token["snowflake"] = fake_user["id"]
        fake_user["user_id"] = fake_user["id"]
        del fake_user["id"]
        self.assertEqual(fake_token, manager.db.get(OAUTH_DATABASE, sess_id))
        self.assertEqual(fake_user, manager.db.get("users", fake_user["user_id"]))

        manager.db.delete(OAUTH_DATABASE, sess_id)
        manager.db.delete("users", fake_user["user_id"])
        manager.db.teardown_request(None)
