from tests import SiteTest

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
