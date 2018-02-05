# coding=utf-8

# External Libraries
from werkzeug.wrappers import Response


class Index:
    path = ["/invite"]

    def get(self):
        return Response(
            status_code=301, text="http://invite.pythondiscord.com/")
