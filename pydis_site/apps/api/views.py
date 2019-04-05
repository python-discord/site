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

    def get(self, request, format=None):  # noqa
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
    def _format_link(description, link, target):
        """
        Build the markup necessary to render `link` with `description`
        as its description in the given `target` language.

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
    def get(self, request, format=None):  # noqa
        link_format = request.query_params.get('link_format', 'md')
        if link_format not in ('html', 'md'):
            raise ParseError(
                f"`format` must be `html` or `md`, got `{format}`."
            )

        discord_community_guidelines_link = self._format_link(
            'Discord Community Guidelines',
            'https://discordapp.com/guidelines',
            link_format
        )
        channels_page_link = self._format_link(
            'channels page',
            'https://pythondiscord.com/about/channels',
            link_format
        )
        google_translate_link = self._format_link(
            'Google Translate',
            'https://translate.google.com/',
            link_format
        )

        return Response([
            "Be polite, and do not spam.",
            f"Follow the {discord_community_guidelines_link}.",
            (
                "Don't intentionally make other people uncomfortable - if "
                "someone asks you to stop discussing something, you should stop."
            ),
            (
                "Be patient both with users asking "
                "questions, and the users answering them."
            ),
            (
                "We will not help you with anything that might break a law or the "
                "terms of service of any other community, pydis_site, service, or "
                "otherwise - No piracy, brute-forcing, captcha circumvention, "
                "sneaker bots, or anything else of that nature."
            ),
            (
                "Listen to and respect the staff members - we're "
                "here to help, but we're all human beings."
            ),
            (
                "All discussion should be kept within the relevant "
                "channels for the subject - See the "
                f"{channels_page_link} for more information."
            ),
            (
                "This is an English-speaking server, so please speak English "
                f"to the best of your ability - {google_translate_link} "
                "should be fine if you're not sure."
            ),
            (
                "Keep all discussions safe for work - No gore, nudity, sexual "
                "soliciting, references to suicide, or anything else of that nature"
            ),
            (
                "We do not allow advertisements for communities (including "
                "other Discord servers) or commercial projects - Contact "
                "us directly if you want to discuss a partnership!"
            )
        ])
