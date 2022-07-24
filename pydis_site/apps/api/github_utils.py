"""Utilities for working with the GitHub API."""
import dataclasses
import datetime
import math
import typing

import httpx
import jwt

from pydis_site import settings

MAX_RUN_TIME = datetime.timedelta(minutes=3)
"""The maximum time allowed before an action is declared timed out."""
ISO_FORMAT_STRING = "%Y-%m-%dT%H:%M:%SZ"
"""The datetime string format GitHub uses."""


class ArtifactProcessingError(Exception):
    """Base exception for other errors related to processing a GitHub artifact."""

    status: int


class UnauthorizedError(ArtifactProcessingError):
    """The application does not have permission to access the requested repo."""

    status = 401


class NotFoundError(ArtifactProcessingError):
    """The requested resource could not be found."""

    status = 404


class ActionFailedError(ArtifactProcessingError):
    """The requested workflow did not conclude successfully."""

    status = 400


class RunTimeoutError(ArtifactProcessingError):
    """The requested workflow run was not ready in time."""

    status = 408


class RunPendingError(ArtifactProcessingError):
    """The requested workflow run is still pending, try again later."""

    status = 202


@dataclasses.dataclass(frozen=True)
class WorkflowRun:
    """
    A workflow run from the GitHub API.

    https://docs.github.com/en/rest/actions/workflow-runs#get-a-workflow-run
    """

    name: str
    head_sha: str
    created_at: str
    status: str
    conclusion: str
    artifacts_url: str

    @classmethod
    def from_raw(cls, data: dict[str, typing.Any]):
        """Create an instance using the raw data from the API, discarding unused fields."""
        return cls(**{
            key.name: data[key.name] for key in dataclasses.fields(cls)
        })


def generate_token() -> str:
    """
    Generate a JWT token to access the GitHub API.

    The token is valid for roughly 10 minutes after generation, before the API starts
    returning 401s.

    Refer to:
    https://docs.github.com/en/developers/apps/building-github-apps/authenticating-with-github-apps#authenticating-as-a-github-app
    """
    now = datetime.datetime.now()
    return jwt.encode(
        {
            "iat": math.floor((now - datetime.timedelta(seconds=60)).timestamp()),  # Issued at
            "exp": math.floor((now + datetime.timedelta(minutes=9)).timestamp()),  # Expires at
            "iss": settings.GITHUB_OAUTH_APP_ID,
        },
        settings.GITHUB_OAUTH_KEY,
        algorithm="RS256"
    )


def authorize(owner: str, repo: str) -> httpx.Client:
    """
    Get an access token for the requested repository.

    The process is roughly:
        - GET app/installations to get a list of all app installations
        - POST <app_access_token> to get a token to access the given app
        - GET installation/repositories and check if the requested one is part of those
    """
    client = httpx.Client(
        base_url=settings.GITHUB_API,
        headers={"Authorization": f"bearer {generate_token()}"},
        timeout=settings.TIMEOUT_PERIOD,
    )

    try:
        # Get a list of app installations we have access to
        apps = client.get("app/installations")
        apps.raise_for_status()

        for app in apps.json():
            # Look for an installation with the right owner
            if app["account"]["login"] != owner:
                continue

            # Get the repositories of the specified owner
            app_token = client.post(app["access_tokens_url"])
            app_token.raise_for_status()
            client.headers["Authorization"] = f"bearer {app_token.json()['token']}"

            repos = client.get("installation/repositories")
            repos.raise_for_status()

            # Search for the request repository
            for accessible_repo in repos.json()["repositories"]:
                if accessible_repo["name"] == repo:
                    # We've found the correct repository, and it's accessible with the current auth
                    return client

        raise NotFoundError(
            "Could not find the requested repository. Make sure the application can access it."
        )

    except BaseException as e:
        # Close the client if we encountered an unexpected exception
        client.close()
        raise e


def check_run_status(run: WorkflowRun) -> str:
    """Check if the provided run has been completed, otherwise raise an exception."""
    created_at = datetime.datetime.strptime(run.created_at, ISO_FORMAT_STRING)
    run_time = datetime.datetime.now() - created_at

    if run.status != "completed":
        if run_time <= MAX_RUN_TIME:
            raise RunPendingError(
                f"The requested run is still pending. It was created "
                f"{run_time.seconds // 60}:{run_time.seconds % 60 :>02} minutes ago."
            )
        else:
            raise RunTimeoutError("The requested workflow was not ready in time.")

    if run.conclusion != "success":
        # The action failed, or did not run
        raise ActionFailedError(f"The requested workflow ended with: {run.conclusion}")

    # The requested action is ready
    return run.artifacts_url


def get_artifact(owner: str, repo: str, sha: str, action_name: str, artifact_name: str) -> str:
    """Get a download URL for a build artifact."""
    client = authorize(owner, repo)

    try:
        # Get the workflow runs for this repository
        runs = client.get(f"/repos/{owner}/{repo}/actions/runs", params={"per_page": 100})
        runs.raise_for_status()
        runs = runs.json()

        # Filter the runs for the one associated with the given SHA
        for run in runs["workflow_runs"]:
            run = WorkflowRun.from_raw(run)
            if run.name == action_name and sha == run.head_sha:
                break
        else:
            raise NotFoundError(
                "Could not find a run matching the provided settings in the previous hundred runs."
            )

        # Check the workflow status
        url = check_run_status(run)

        # Filter the artifacts, and return the download URL
        artifacts = client.get(url)
        artifacts.raise_for_status()

        for artifact in artifacts.json()["artifacts"]:
            if artifact["name"] == artifact_name:
                data = client.get(artifact["archive_download_url"])
                if data.status_code == 302:
                    return str(data.next_request.url)

                # The following line is left untested since it should in theory be impossible
                data.raise_for_status()  # pragma: no cover

        raise NotFoundError("Could not find an artifact matching the provided name.")

    finally:
        client.close()
