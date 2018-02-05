# coding=utf-8

# External Libraries
from werkzeug.wrappers import Response

# Site Internals
import ujson as json


class Index:
    path = ["/healthcheck"]

    def get(self):
        return Response(json.dumps({"status": "ok"}))
