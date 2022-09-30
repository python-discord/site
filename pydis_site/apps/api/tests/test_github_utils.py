import dataclasses
import datetime
import typing
import unittest
from unittest import mock

import django.test
import httpx
import jwt
import rest_framework.response
import rest_framework.test
from django.urls import reverse

from .. import github_utils


class GeneralUtilityTests(unittest.TestCase):
    """Test the utility methods which do not fit in another class."""

    def test_token_generation(self):
        """Test that the a valid JWT token is generated."""
        def encode(payload: dict, _: str, algorithm: str, *args, **kwargs) -> str:
            """
            Intercept the encode method.

            The result is encoded with an algorithm which does not require a PEM key, as it may
            not be available in testing environments.
            """
            self.assertEqual("RS256", algorithm, "The GitHub App JWT must be signed using RS256.")
            return original_encode(
                payload, "secret-encoding-key", *args, algorithm="HS256", **kwargs
            )

        original_encode = jwt.encode
        with mock.patch("jwt.encode", new=encode):
            token = github_utils.generate_token()
        decoded = jwt.decode(token, "secret-encoding-key", algorithms=["HS256"])

        delta = datetime.timedelta(minutes=10)
        self.assertAlmostEqual(decoded["exp"] - decoded["iat"], delta.total_seconds())
        self.assertLess(decoded["exp"], (datetime.datetime.now() + delta).timestamp())


class CheckRunTests(unittest.TestCase):
    """Tests the check_run_status utility."""

    run_kwargs: typing.Mapping = {
        "name": "run_name",
        "head_sha": "sha",
        "status": "completed",
        "conclusion": "success",
        "created_at": datetime.datetime.utcnow().strftime(github_utils.ISO_FORMAT_STRING),
        "artifacts_url": "url",
    }

    def test_completed_run(self):
        """Test that an already completed run returns the correct URL."""
        final_url = "some_url_string_1234"

        kwargs = dict(self.run_kwargs, artifacts_url=final_url)
        result = github_utils.check_run_status(github_utils.WorkflowRun(**kwargs))
        self.assertEqual(final_url, result)

    def test_pending_run(self):
        """Test that a pending run raises the proper exception."""
        kwargs = dict(self.run_kwargs, status="pending")
        with self.assertRaises(github_utils.RunPendingError):
            github_utils.check_run_status(github_utils.WorkflowRun(**kwargs))

    def test_timeout_error(self):
        """Test that a timeout is declared after a certain duration."""
        kwargs = dict(self.run_kwargs, status="pending")
        # Set the creation time to well before the MAX_RUN_TIME
        # to guarantee the right conclusion
        kwargs["created_at"] = (
            datetime.datetime.utcnow() - github_utils.MAX_RUN_TIME - datetime.timedelta(minutes=10)
        ).strftime(github_utils.ISO_FORMAT_STRING)

        with self.assertRaises(github_utils.RunTimeoutError):
            github_utils.check_run_status(github_utils.WorkflowRun(**kwargs))

    def test_failed_run(self):
        """Test that a failed run raises the proper exception."""
        kwargs = dict(self.run_kwargs, conclusion="failed")
        with self.assertRaises(github_utils.ActionFailedError):
            github_utils.check_run_status(github_utils.WorkflowRun(**kwargs))


def get_response_authorize(_: httpx.Client, request: httpx.Request, **__) -> httpx.Response:
    """
    Helper method for the authorize tests.

    Requests are intercepted before being sent out, and the appropriate responses are returned.
    """
    path = request.url.path
    auth = request.headers.get("Authorization")

    if request.method == "GET":
        if path == "/app/installations":
            if auth == "bearer JWT initial token":
                return httpx.Response(200, request=request, json=[{
                    "account": {"login": "VALID_OWNER"},
                    "access_tokens_url": "https://example.com/ACCESS_TOKEN_URL"
                }])
            else:
                return httpx.Response(
                    401, json={"error": "auth app/installations"}, request=request
                )

        elif path == "/installation/repositories":
            if auth == "bearer app access token":
                return httpx.Response(200, request=request, json={
                    "repositories": [{
                        "name": "VALID_REPO"
                    }]
                })
            else:  # pragma: no cover
                return httpx.Response(
                    401, json={"error": "auth installation/repositories"}, request=request
                )

    elif request.method == "POST":
        if path == "/ACCESS_TOKEN_URL":
            if auth == "bearer JWT initial token":
                return httpx.Response(200, request=request, json={"token": "app access token"})
            else:  # pragma: no cover
                return httpx.Response(401, json={"error": "auth access_token"}, request=request)

    # Reaching this point means something has gone wrong
    return httpx.Response(500, request=request)  # pragma: no cover


@mock.patch("httpx.Client.send", new=get_response_authorize)
@mock.patch.object(github_utils, "generate_token", new=mock.Mock(return_value="JWT initial token"))
class AuthorizeTests(unittest.TestCase):
    """Test the authorize utility."""

    def test_invalid_apps_auth(self):
        """Test that an exception is raised if authorization was attempted with an invalid token."""
        with mock.patch.object(github_utils, "generate_token", return_value="Invalid token"):
            with self.assertRaises(httpx.HTTPStatusError) as error:
                github_utils.authorize("VALID_OWNER", "VALID_REPO")

        exception: httpx.HTTPStatusError = error.exception
        self.assertEqual(401, exception.response.status_code)
        self.assertEqual("auth app/installations", exception.response.json()["error"])

    def test_missing_repo(self):
        """Test that an exception is raised when the selected owner or repo are not available."""
        with self.assertRaises(github_utils.NotFoundError):
            github_utils.authorize("INVALID_OWNER", "VALID_REPO")
        with self.assertRaises(github_utils.NotFoundError):
            github_utils.authorize("VALID_OWNER", "INVALID_REPO")

    def test_valid_authorization(self):
        """Test that an accessible repository can be accessed."""
        client = github_utils.authorize("VALID_OWNER", "VALID_REPO")
        self.assertEqual("bearer app access token", client.headers.get("Authorization"))


class ArtifactFetcherTests(unittest.TestCase):
    """Test the get_artifact utility."""

    @staticmethod
    def get_response_get_artifact(request: httpx.Request, **_) -> httpx.Response:
        """
        Helper method for the get_artifact tests.

        Requests are intercepted before being sent out, and the appropriate responses are returned.
        """
        path = request.url.path

        if "force_error" in path:
            return httpx.Response(404, request=request)

        if request.method == "GET":
            if path == "/repos/owner/repo/actions/runs":
                run = github_utils.WorkflowRun(
                    name="action_name",
                    head_sha="action_sha",
                    created_at=datetime.datetime.now().strftime(github_utils.ISO_FORMAT_STRING),
                    status="completed",
                    conclusion="success",
                    artifacts_url="artifacts_url"
                )
                return httpx.Response(
                    200, request=request, json={"workflow_runs": [dataclasses.asdict(run)]}
                )
            elif path == "/artifact_url":
                return httpx.Response(
                    200, request=request, json={"artifacts": [{
                        "name": "artifact_name",
                        "archive_download_url": "artifact_download_url"
                    }]}
                )
            elif path == "/artifact_download_url":
                response = httpx.Response(302, request=request)
                response.next_request = httpx.Request(
                    "GET",
                    httpx.URL("https://final_download.url")
                )
                return response

        # Reaching this point means something has gone wrong
        return httpx.Response(500, request=request)  # pragma: no cover

    def setUp(self) -> None:
        self.call_args = ["owner", "repo", "action_sha", "action_name", "artifact_name"]
        self.client = httpx.Client(base_url="https://example.com")

        self.patchers = [
            mock.patch.object(self.client, "send", new=self.get_response_get_artifact),
            mock.patch.object(github_utils, "authorize", return_value=self.client),
            mock.patch.object(github_utils, "check_run_status", return_value="artifact_url"),
        ]

        for patcher in self.patchers:
            patcher.start()

    def tearDown(self) -> None:
        for patcher in self.patchers:
            patcher.stop()

    def test_client_closed_on_errors(self):
        """Test that the client is terminated even if an error occurs at some point."""
        self.call_args[0] = "force_error"
        with self.assertRaises(httpx.HTTPStatusError):
            github_utils.get_artifact(*self.call_args)
        self.assertTrue(self.client.is_closed)

    def test_missing(self):
        """Test that an exception is raised if the requested artifact was not found."""
        cases = (
            "invalid sha",
            "invalid action name",
            "invalid artifact name",
        )
        for i, name in enumerate(cases, 2):
            with self.subTest(f"Test {name} raises an error"):
                new_args = self.call_args.copy()
                new_args[i] = name

                with self.assertRaises(github_utils.NotFoundError):
                    github_utils.get_artifact(*new_args)

    def test_valid(self):
        """Test that the correct download URL is returned for valid requests."""
        url = github_utils.get_artifact(*self.call_args)
        self.assertEqual("https://final_download.url", url)
        self.assertTrue(self.client.is_closed)


@mock.patch.object(github_utils, "get_artifact")
class GitHubArtifactViewTests(django.test.TestCase):
    """Test the GitHub artifact fetch API view."""

    def setUp(self):
        self.kwargs = {
            "owner": "test_owner",
            "repo": "test_repo",
            "sha": "test_sha",
            "action_name": "test_action",
            "artifact_name": "test_artifact",
        }
        self.url = reverse("api:github-artifacts", kwargs=self.kwargs)

    def test_correct_artifact(self, artifact_mock: mock.Mock):
        """Test a proper response is returned with proper input."""
        artifact_mock.return_value = "final download url"
        result = self.client.get(self.url)

        self.assertIsInstance(result, rest_framework.response.Response)
        self.assertEqual({"url": artifact_mock.return_value}, result.data)

    def test_failed_fetch(self, artifact_mock: mock.Mock):
        """Test that a proper error is returned when the request fails."""
        artifact_mock.side_effect = github_utils.NotFoundError("Test error message")
        result = self.client.get(self.url)

        self.assertIsInstance(result, rest_framework.response.Response)
        self.assertEqual({
            "error_type": github_utils.NotFoundError.__name__,
            "error": "Test error message",
            "requested_resource": "/".join(self.kwargs.values())
        }, result.data)
