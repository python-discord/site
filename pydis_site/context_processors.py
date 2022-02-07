from django.http import HttpRequest

from pydis_site.constants import GIT_SHA


def git_sha_processor(_: HttpRequest) -> dict:
    """Expose the git SHA for this repo to all views."""
    return {'git_sha': GIT_SHA}
