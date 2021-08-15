import inspect
from pathlib import Path

from django.http import HttpRequest
from django.template import RequestContext

from pydis_site.constants import GIT_SHA


def git_sha_processor(_: HttpRequest) -> dict:
    """Expose the git SHA for this repo to all views."""
    return {'git_sha': GIT_SHA}


def path_processor(_: HttpRequest) -> dict:
    """Expose each view's path to itself."""
    # This is a disgusting hack, here's how it works in detail:
    #
    # 1. We use inspect to pull all the local variables from the previous frame, and access self
    #   1a. The previous frame is a django internal which calls context processors,
    #   and has access to the template
    #   1b. The caller is a method in RequestContext, hence self is an instance of RequestContext
    #
    # 2. We use RequestContext.template to get the Template object,
    #    which has an absolute path to the template
    #
    # 3. We use pathlib to create a relative path to the root directory of the project

    context: RequestContext = inspect.currentframe().f_back.f_locals["self"]

    path = Path(context.template.origin.name).relative_to(Path.cwd())
    return {"path": path}
