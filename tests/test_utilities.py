from tests import SiteTest, manager

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
