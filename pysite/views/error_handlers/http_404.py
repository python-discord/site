# coding=utf-8
from werkzeug.exceptions import NotFound

from pysite.base_route import ErrorView


class Error404View(ErrorView):
    name = "error_404"
    error_code = 404
    description = "This is not the page you're looking for... (status 404)"

    def get(self, error: NotFound):
        print("Called!")
        return self.render('error.html', description=self.description), 404
