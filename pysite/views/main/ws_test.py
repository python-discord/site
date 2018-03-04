# coding=utf-8
import os

from pysite.base_route import RouteView


class WSTest(RouteView):
    path = "/ws_test"
    name = "ws_test"

    def get(self):
        return self.render(
            "main/ws_test.html",
            server_name=os.environ.get("SERVER_NAME", "localhost")
        )
