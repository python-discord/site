import json
import logging
import urllib.request
from collections.abc import Mapping
from http import HTTPStatus

from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from . import github_utils


class HealthcheckView(APIView):
    """
    Provides a simple view to check that the website is alive and well.

    ## Routes
    ### GET /healthcheck
    Returns a simple JSON document showcasing whether the system is working:

    >>> {
    ...     'status': 'ok'
    ... }

    Seems to be.

    ## Authentication
    Does not require any authentication nor permissions.
    """

    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):  # noqa: D102,ANN001,ANN201
        return Response({'status': 'ok'})


class RulesView(APIView):
    """
    Return a list of the server's rules.

    ## Routes
    ### GET /rules
    Returns a JSON array containing the server's rules
    and keywords relating to each rule.
    Example response:

    >>> [
    ...     ["Eat candy.", ["candy", "sweets"]],
    ...     ["Wake up at 4 AM.", ["wake_up", "early", "early_bird"]],
    ...     ["Take your medicine.", ["medicine", "health"]]
    ... ]

    Since some of the the rules require links, this view
    gives you the option to return rules in either Markdown
    or HTML format by specifying the `link_format` query parameter
    as either `md` or `html`. Specifying a different value than
    `md` or `html` will return 400.

    ## Authentication
    Does not require any authentication nor permissions.
    """

    authentication_classes = ()
    permission_classes = ()

    @staticmethod
    def _format_link(description: str, link: str, target: str) -> str:
        """
        Build the markup for rendering the link.

        This will render `link` with `description` as its description in the given
        `target` language.

        Arguments:
            description (str):
                A textual description of the string. Represents the content
                between the `<a>` tags in HTML, or the content between the
                array brackets in Markdown.

            link (str):
                The resulting link that a user should be redirected to
                upon clicking the generated element.

            target (str):
                One of `{'md', 'html'}`, denoting the target format that the
                link should be rendered in.

        Returns:
            str:
                The link, rendered appropriately for the given `target` format
                using `description` as its textual description.

        Raises:
            ValueError:
                If `target` is not `'md'` or `'html'`.
        """
        if target == 'html':
            return f'<a href="{link}">{description}</a>'
        elif target == 'md':  # noqa: RET505
            return f'[{description}]({link})'
        else:
            raise ValueError(
                f"Can only template links to `html` or `md`, got `{target}`"
            )

    # `format` here is the result format, we have a link format here instead.
    def get(self, request, format=None):  # noqa: ANN001, ANN201
        """
        Returns a list of our community rules coupled with their keywords.

        Each item in the returned list is a tuple with the rule as first item
        and a list of keywords that match that rules as second item.
        """
        link_format = request.query_params.get('link_format', 'md')
        if link_format not in ('html', 'md'):
            raise ParseError(
                f"`format` must be `html` or `md`, got `{format}`."
            )

        discord_community_guidelines = self._format_link(
            'Discord Community Guidelines',
            'https://discordapp.com/guidelines',
            link_format
        )
        discord_tos = self._format_link(
            'Terms of Service',
            'https://discordapp.com/terms',
            link_format
        )
        pydis_coc = self._format_link(
            'Python Discord Code of Conduct',
            'https://pythondiscord.com/pages/code-of-conduct/',
            link_format
        )

        return Response([
            (
                f"Follow the {pydis_coc}.",
                ["coc", "conduct", "code"]
            ),
            (
                f"Follow the {discord_community_guidelines} and {discord_tos}.",
                ["discord", "guidelines", "discord_tos"]
            ),
            (
                "Respect staff members and listen to their instructions.",
                ["respect", "staff", "instructions"]
            ),
            (
                "Use English to the best of your ability. "
                "Be polite if someone speaks English imperfectly.",
                ["english", "eng", "language"]
            ),
            (
                "Do not provide or request help on projects that may violate terms of service, "
                "or that may be deemed inappropriate, malicious, or illegal.",
                ["infraction", "tos", "breach", "malicious", "inappropriate", "illegal"]
            ),
            (
                "Do not post unapproved advertising.",
                ["ad", "ads", "advert", "advertising"]
            ),
            (
                "Keep discussions relevant to the channel topic. "
                "Each channel's description tells you the topic.",
                ["off-topic", "topic", "relevance"]
            ),
            (
                "Do not help with ongoing exams. When helping with homework, "
                "help people learn how to do the assignment without doing it for them.",
                ["exam", "exams", "assignment", "assignments", "homework", "hw"]
            ),
            (
                "Do not offer or ask for paid work of any kind.",
                ["pay", "paid", "work", "money", "hire"]
            ),
            (
                "Do not copy and paste answers from ChatGPT or similar AI tools.",
                ["gpt", "chatgpt", "gpt3", "ai"]
            ),
        ])


class GitHubArtifactsView(APIView):
    """
    Provides utilities for interacting with the GitHub API and obtaining action artifacts.

    ## Routes
    ### GET /github/artifacts
    Returns a download URL for the artifact requested.

        {
            'url': 'https://pipelines.actions.githubusercontent.com/...'
        }

    ### Exceptions
    In case of an error, the following body will be returned:

        {
            "error_type": "<error class name>",
            "error": "<error description>",
            "requested_resource": "<owner>/<repo>/<sha>/<artifact_name>"
        }

    ## Authentication
    Does not require any authentication nor permissions.
    """

    authentication_classes = ()
    permission_classes = ()

    def get(
        self,
        request: Request,
        *,
        owner: str,
        repo: str,
        sha: str,
        action_name: str,
        artifact_name: str
    ) -> Response:
        """Return a download URL for the requested artifact."""
        try:
            url = github_utils.get_artifact(owner, repo, sha, action_name, artifact_name)
            return Response({"url": url})
        except github_utils.ArtifactProcessingError as e:
            return Response({
                "error_type": e.__class__.__name__,
                "error": str(e),
                "requested_resource": f"{owner}/{repo}/{sha}/{action_name}/{artifact_name}"
            }, status=e.status)


class GitHubWebhookFilterView(APIView):
    """
    Filters uninteresting events from webhooks sent by GitHub to Discord.

    ## Routes
    ### POST /github/webhook-filter/:webhook_id/:webhook_token
    Takes the GitHub webhook payload as the request body, documented on here:
    https://docs.github.com/en/webhooks/webhook-events-and-payloads. The endpoint
    will then determine whether the sent webhook event is of interest,
    and if so, will forward it to Discord. The response from Discord is
    then returned back to the client of this website, including the original
    status code and headers (excluding `Content-Type`).

    ## Authentication
    Does not require any authentication nor permissions on its own, however,
    Discord will validate that the webhook originates from GitHub and respond
    with a 403 forbidden error if not.
    """

    authentication_classes = ()
    permission_classes = ()
    logger = logging.getLogger(__name__ + ".GitHubWebhookFilterView")

    def post(self, request: Request, *, webhook_id: str, webhook_token: str) -> Response:
        """Filter a webhook POST from GitHub before sending it to Discord."""
        sender = request.data.get('sender', {})
        sender_name = sender.get('login', '').lower()
        event = request.headers.get('X-GitHub-Event', '').lower()
        repository = request.data.get('repository', {})

        is_coveralls = 'coveralls' in sender_name
        is_github_bot = sender.get('type', '').lower() == 'bot'
        is_sentry = 'sentry-io' in sender_name
        is_dependabot_branch_deletion = (
            'dependabot' in request.data.get('ref', '').lower()
            and event == 'delete'
        )
        is_bot_pr_approval = is_github_bot and event == 'pull_request_review'
        is_empty_review = (
            request.data.get('review', {}).get('state', '').lower() == 'commented'
            and event == 'pull_request_review'
            and request.data.get('review', {}).get('body') is None
        )
        is_black_non_main_push = (
            request.data.get('ref') != 'refs/heads/main'
            and repository.get('name', '').lower() == 'black'
            and repository.get('owner', {}).get('login', '').lower() == 'psf'
            and event == 'push'
        )

        is_bot_payload = (
            is_coveralls
            or (is_github_bot and not is_sentry)
            or is_dependabot_branch_deletion
            or is_bot_pr_approval
        )
        is_noisy_user_action = is_empty_review
        should_ignore = is_bot_payload or is_noisy_user_action or is_black_non_main_push

        if should_ignore:
            return Response(
                {'message': "Ignored by github-filter endpoint"},
                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            )

        (response_status, headers, body) = self.send_webhook(
            webhook_id, webhook_token, request.data, dict(request.headers),
        )
        headers.pop('Connection', None)
        headers.pop('Content-Length', None)
        return Response(data=body, headers=headers, status=response_status)

    def send_webhook(
        self,
        webhook_id: str,
        webhook_token: str,
        data: dict,
        headers: Mapping[str, str],
    ) -> tuple[int, dict[str, str], bytes]:
        """Execute a webhook on Discord's GitHub webhook endpoint."""
        payload = json.dumps(data).encode()
        headers.pop('Content-Length', None)
        headers.pop('Content-Type', None)
        headers.pop('Host', None)
        request = urllib.request.Request(  # noqa: S310
            f'https://discord.com/api/webhooks/{webhook_id}/{webhook_token}/github?wait=1',
            data=payload,
            headers={'Content-Type': 'application/json', **headers},
        )

        try:
            with urllib.request.urlopen(request) as response:  # noqa: S310
                return (response.status, dict(response.getheaders()), response.read())
        except urllib.error.HTTPError as err:  # pragma: no cover
            if err.code == HTTPStatus.TOO_MANY_REQUESTS:
                self.logger.warning(
                    "We are being rate limited by Discord! Scope: %s, reset-after: %s",
                    headers.get("X-RateLimit-Scope"),
                    headers.get("X-RateLimit-Reset-After"),
                )
            return (err.code, dict(err.headers), err.fp.read())
