from tests import SiteTest, manager

class Utilities(SiteTest):
    """ Test cases for internal utility code """
    def test_error_view_runtime_error(self):
        """ Check that wrong values for error view setup raises runtime error """
        import pysite.base_route

        ev = pysite.base_route.ErrorView()

        with self.assertRaises(RuntimeError):
            ev.setup(manager, 'sdfsdf')

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
