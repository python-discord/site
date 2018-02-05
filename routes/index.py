# coding=utf-8

# External Libraries
from werkzeug.wrappers import Response


class Index:
    path = ["/", "/index"]

    def get(self):
        return Response("Coming soon:tm:")
