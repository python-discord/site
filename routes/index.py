# coding=utf-8


class Index:
    path = ["/", "/index"]

    def get(self, req):
        return req.Response("Coming soon:tm:")
