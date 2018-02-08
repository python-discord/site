# coding=utf-8
from pysite.base_route import BaseView


class IndexView(BaseView):
    path = "/"
    name = "index"

    def get(self):
        return "Coming soon:tm:"
