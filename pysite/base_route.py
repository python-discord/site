from collections import Iterable
from datetime import datetime
from typing import Any

from flask import Blueprint, Response, jsonify, redirect, render_template, session, url_for
from flask.views import MethodView
from werkzeug.exceptions import default_exceptions

from pysite.constants import ALL_STAFF_ROLES, DEBUG_MODE, ErrorCodes
from pysite.mixins import OAuthMixin


class BaseView(MethodView, OAuthMixin):
    """
    Base view class with functions and attributes that should be common to all view classes.

    This class should be subclassed, and is not intended to be used directly.
    """

    name = None  # type: str
    blueprint = None  # type: str

    def render(self, *template_names: str, **context: Any) -> str:
        """
        Render some templates and get them back in a form that you can simply return from your view function.

        Here's what's inserted:
        * "current_page" - the "name" attribute from the view class
        * "view" - the view class instance
        * "logged_in" - a boolean, True if the user is logged in
        * "static_file(filename)", a function used to get the URL for a given static file
        * "csrf_token()", a function returning the CSRF token stored in the current session

        For XSS protection, a CSRF token must be used. The "csrf_token()" function returns the correct token
        to be used in the current rendering context - if your view methods are to be protected from XSS
        exploits, the following steps must be taken:

        1. Apply the "csrf" decorator to the view method
        2. For forms, a hidden input must be declared in the template, with the name "csrf_token", and the value set to
           the CSRF token.
        3. For any AJAX work, the CSRF token should be stored in a variable, and sent as part of the request headers.
           You can set the "X-CSRFToken" header to the CSRF token for this.

        Any API call or form submission not protected by an API key must not be vulnerable to XSS, unless the API
        call is intended to be a completely public feature. Public API methods must not be account-bound, and they
        must never return information on a current user or perform any action. Only data retrieval is permissible.

        :param template_names: Names of the templates to render
        :param context: Extra data to pass into the template
        :return: String representing the rendered templates
        """

        context["current_page"] = self.name
        context["view"] = self
        context["logged_in"] = self.logged_in
        context["user"] = self.user_data
        context["static_file"] = self._static_file
        context["debug"] = DEBUG_MODE
        context["format_datetime"] = lambda dt: dt.strftime("%b %d %Y, %H:%M") if isinstance(dt, datetime) else dt
        context["blueprint"] = self.blueprint

        def is_staff():
            if DEBUG_MODE:
                return True

            if not self.logged_in:
                return False

            for role in ALL_STAFF_ROLES:
                if role in self.user_data.get("roles", []):
                    return True

            return False

        context["is_staff"] = is_staff

        return render_template(template_names, **context)

    def _static_file(self, filename):
        return url_for("static", filename=filename)


class RouteView(BaseView):
    """
    Standard route-based page view. For a standard page, this is what you want.

    This class is intended to be subclassed - use it as a base class for your own views, and set the class-level
    attributes as appropriate. For example:

    >>> class MyView(RouteView):
    ...     name = "my_view"  # Flask internal name for this route
    ...     path = "/my_view"  # Actual URL path to reach this route
    ...
    ...     def get(self):  # Name your function after the relevant HTTP method
    ...         return self.render("index.html")

    For more complicated routing, see http://exploreflask.com/en/latest/views.html#built-in-converters
    """

    path = None  # type: str

    @classmethod
    def setup(cls: "RouteView", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        """
        Set up the view by adding it to the blueprint passed in - this will also deal with multiple inheritance by
        calling `super().setup()` as appropriate.

        This is for a standard route view. Nothing special here.

        :param manager: Instance of the current RouteManager
        :param blueprint: Current Flask blueprint to register this route to
        """

        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)

        if not cls.path or not cls.name:
            raise RuntimeError("Route views must have both `path` and `name` defined")

        blueprint.add_url_rule(cls.path, view_func=cls.as_view(cls.name))

        cls.blueprint = blueprint.name
        cls.name = f"{blueprint.name}.{cls.name}"  # Add blueprint to page name

    def redirect_login(self, **kwargs):
        session["redirect_target"] = {
            "url": self.name,
            "kwargs": kwargs
        }

        response = redirect(url_for("discord.login"))
        response.headers.add("X-Robots-Tag", "noindex")

        return response


class APIView(RouteView):
    """
    API route view, with extra methods to help you add routes to the JSON API with ease.

    This class is intended to be subclassed - use it as a base class for your own views, and set the class-level
    attributes as appropriate. For example:

    >>> class MyView(APIView):
    ...     name = "my_view"  # Flask internal name for this route
    ...     path = "/my_view"  # Actual URL path to reach this route
    ...
    ...     def get(self):  # Name your function after the relevant HTTP method
    ...         return self.error(ErrorCodes.unknown_route)
    """

    def error(self, error_code: ErrorCodes, error_info: str = "") -> Response:
        """
        Generate a JSON response for you to return from your handler, for a specific type of API error

        :param error_code: The type of error to generate a response for - see `constants.ErrorCodes` for more
        :param error_info: An optional message with more information about the error.
        :return: A Flask Response object that you can return from your handler
        """

        data = {
            "error_code": error_code.value,
            "error_message": error_info or "Unknown error"
        }

        http_code = 200

        if error_code is ErrorCodes.unknown_route:
            data["error_message"] = error_info or "Unknown API route"
            http_code = 404
        elif error_code is ErrorCodes.unauthorized:
            data["error_message"] = error_info or "Unauthorized"
            http_code = 401
        elif error_code is ErrorCodes.invalid_api_key:
            data["error_message"] = error_info or "Invalid API-key"
            http_code = 401
        elif error_code is ErrorCodes.bad_data_format:
            data["error_message"] = error_info or "Input data in incorrect format"
            http_code = 400
        elif error_code is ErrorCodes.incorrect_parameters:
            data["error_message"] = error_info or "Incorrect parameters provided"
            http_code = 400

        response = jsonify(data)
        response.status_code = http_code
        return response


class ErrorView(BaseView):
    """
    Error view, shown for a specific HTTP status code, as defined in the class attributes.

    This class is intended to be subclassed - use it as a base class for your own views, and set the class-level
    attributes as appropriate. For example:

    >>> class MyView(ErrorView):
    ...     name = "my_view"  # Flask internal name for this route
    ...     path = "/my_view"  # Actual URL path to reach this route
    ...     error_code = 404  # Error code
    ...
    ...     def get(self, error: HTTPException):  # Name your function after the relevant HTTP method
    ...         return "Replace me with a template, 404 not found", 404

    If you'd like to catch multiple HTTP error codes, feel free to supply an iterable for `error_code`. For example...

    >>> error_code = [401, 403]  # Handle two specific errors
    >>> error_code = range(500, 600)  # Handle all 5xx errors
    """

    error_code = None  # type: Union[int, Iterable]
    register_on_app = True
    blueprint = "error"  # Because it doesn't truly have its own

    @classmethod
    def setup(cls: "ErrorView", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        """
        Set up the view by registering it as the error handler for the HTTP status codes specified in the class
        attributes - this will also deal with multiple inheritance by calling `super().setup()` as appropriate.

        :param manager: Instance of the current RouteManager
        :param blueprint: Current Flask blueprint to register the error handler for
        """

        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)  # pragma: no cover

        if not cls.name or not cls.error_code:
            raise RuntimeError("Error views must have both `name` and `error_code` defined")

        if isinstance(cls.error_code, int):
            cls.error_code = [cls.error_code]

        if isinstance(cls.error_code, Iterable):
            for code in cls.error_code:
                if isinstance(code, int) and code not in default_exceptions:
                    continue  # Otherwise we'll possibly get an exception thrown during blueprint registration

                if cls.register_on_app:
                    manager.app.errorhandler(code)(cls.as_view(cls.name))
                else:
                    blueprint.errorhandler(code)(cls.as_view(cls.name))
        else:
            raise RuntimeError(
                "Error views must have an `error_code` that is either an `int` or an iterable")  # pragma: no cover # noqa: E501


class TemplateView(RouteView):
    """
    An easy view for routes that simply render a template with no extra information.

    This class is intended to be subclassed - use it as a base class for your own views, and set the class-level
    attributes as appropriate. For example:

    >>> class MyView(TemplateView):
    ...     name = "my_view"  # Flask internal name for this route
    ...     path = "/my_view"  # Actual URL path to reach this route
    ...     template = "my_view.html"  # Template to use

    Note that this view only handles GET requests. If you need any other verbs, you can implement them yourself
    or just use one of the more customizable base view classes.
    """

    template = None  # type: str

    @classmethod
    def setup(cls: "TemplateView", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        """
        Set up the view, deferring most setup to the superclasses but checking for the template attribute.

        :param manager: Instance of the current RouteManager
        :param blueprint: Current Flask blueprint to register the error handler for
        """

        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)  # pragma: no cover

        if not cls.template:
            raise RuntimeError("Template views must have `template` defined")

    def get(self, *_):
        return self.render(self.template)


class RedirectView(RouteView):
    """
    An easy view for routes that simply redirect to another page or view.

    This class is intended to be subclassed - use it as a base class for your own views, and set the class-level
    attributes as appropriate. For example:

    >>> class MyView(RedirectView):
    ...     name = "my_view"  # Flask internal name for this route
    ...     path = "/my_view"  # Actual URL path to reach this route
    ...     code = 303  # HTTP status code to use for the redirect; 303 by default
    ...     page = "staff.index"  # Page to redirect to
    ...     kwargs = {}  # Any extra keyword args to pass to the url_for call, if redirecting to another view

    You can specify a full URL, including the protocol, eg "http://google.com" or a Flask internal route name,
    eg "main.index". Nothing else is supported.

    Note that this view only handles GET requests. If you need any other verbs, you can implement them yourself
    or just use one of the more customizable base view classes.
    """

    code = 303  # type: int
    page = None  # type: str
    kwargs = {}  # type: Optional[dict]

    @classmethod
    def setup(cls: "RedirectView", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        """
        Set up the view, deferring most setup to the superclasses but checking for the template attribute.

        :param manager: Instance of the current RouteManager
        :param blueprint: Current Flask blueprint to register the error handler for
        """

        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)  # pragma: no cover

        if not cls.page or not cls.code:
            raise RuntimeError("Redirect views must have both `code` and `page` defined")

    def get(self, *_):
        if "://" in self.page:
            return redirect(self.page, code=self.code)

        return redirect(url_for(self.page, **self.kwargs), code=self.code)
