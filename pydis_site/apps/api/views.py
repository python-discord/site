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
                ["pay", "paid", "work", "money"]
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
