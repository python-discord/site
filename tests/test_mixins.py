import os
from tests import SiteTest, manager

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

        with self.assertRaises(RuntimeError):
            rv.setup(manager, 'sdfsdf')

    def test_oauth_property(self):
        """ Make sure the oauth property works"""
        from flask import Blueprint

        from pysite.route_manager import RouteView
        from pysite.oauth import OAuthBackend

        class TestRoute(RouteView):
            name = "test"
            path = "/test"

        tr = TestRoute()
        tr.setup(manager, Blueprint("test", "test_name"))
        self.assertIsInstance(tr.oauth, OAuthBackend)

    def test_user_data_property(self):
        """ Make sure the user_data property works"""
        from flask import Blueprint

        from pysite.route_manager import RouteView

        class TestRoute(RouteView):
            name = "test"
            path = "/test"

        tr = TestRoute()
        tr.setup(manager, Blueprint("test", "test_name"))
        self.assertIsNone(tr.user_data)

    def test_logged_in_property(self):
        """ Make sure the user_data property works"""
        from flask import Blueprint

        from pysite.route_manager import RouteView

        class TestRoute(RouteView):
            name = "test"
            path = "/test"

        tr = TestRoute()
        tr.setup(manager, Blueprint("test", "test_name"))
        self.assertFalse(tr.logged_in)
