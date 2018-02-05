# coding=utf-8

# External Libraries
from werkzeug.wrappers import Response


class Index:
    error_code = 404

    def err(self):
        return Response("Page not found!", 404)
