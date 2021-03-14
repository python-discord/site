from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView


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
    Returns a JSON array containing the server's rules:

    >>> [
    ...     "Eat candy.",
    ...     "Wake up at 4 AM.",
    ...     "Take your medicine."
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
        elif target == 'md':
            return f'[{description}]({link})'
        else:
            raise ValueError(
                f"Can only template links to `html` or `md`, got `{target}`"
            )

    # `format` here is the result format, we have a link format here instead.
    def get(self, request, format=None):  # noqa: D102,ANN001,ANN201
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
            'Terms Of Service',
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
                f"Follow the {discord_community_guidelines} and {discord_tos}."
            ),
            (
                f"Follow the {pydis_coc}."
            ),
            (
                "Listen to and respect staff members and their instructions."
            ),
            (
                "This is an English-speaking server, "
                "so please speak English to the best of your ability."
            ),
            (
                "Do not provide or request help on projects that may break laws, "
                "breach terms of services, be considered malicious or inappropriate. "
                "Do not help with ongoing exams. Do not provide or request solutions "
                "for graded assignments, although general guidance is okay."
            ),
            (
                "No spamming or unapproved advertising, including requests for paid work. "
                "Open-source projects can be shared with others in #python-general and "
                "code reviews can be asked for in a help channel."
            ),
            (
                "Keep discussions relevant to channel topics and guidelines."
            ),
        ])
