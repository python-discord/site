# coding=utf-8


class Index:
    error_code = 404

    def err(self, req):
        return req.Response(text="Page not found!", code=404)
