import os

from pysite.base_route import RouteView


class WSTest(RouteView):
    path = "/ws_test_rst"
    name = "ws_test_rst"

    def get(self):
        return self.render(
            "main/ws_test_rst.html",
            server_name=os.environ.get("SERVER_NAME", "localhost")
        )
