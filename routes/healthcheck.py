# coding=utf-8


class Index:
    path = ["/healthcheck"]

    def get(self, req):
        return req.Response(json={"status": "ok"})
