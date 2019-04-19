from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot.tag import Tag
from pydis_site.apps.api.serializers import TagSerializer


class TagViewSet(ModelViewSet):
    """
    View providing CRUD operations on tags shown by our bot.

    ## Routes
    ### GET /bot/tags
    Returns all tags in the database.

    #### Response format
    >>> [
    ...     {
    ...         'title': "resources",
    ...         'embed': {
    ...             'content': "Did you really think I'd put something useful here?"
    ...         }
    ...     }
    ... ]

    #### Status codes
    - 200: returned on success

    ### GET /bot/tags/<title:str>
    Gets a single tag by its title.

    #### Response format
    >>> {
    ...     'title': "My awesome tag",
    ...     'embed': {
    ...         'content': "totally not filler words"
    ...     }
    ... }

    #### Status codes
    - 200: returned on success
    - 404: if a tag with the given `title` could not be found

    ### POST /bot/tags
    Adds a single tag to the database.

    #### Request body
    >>> {
    ...     'title': str,
    ...     'embed': dict
    ... }

    The embed structure is the same as the embed structure that the Discord API
    expects. You can view the documentation for it here:
        https://discordapp.com/developers/docs/resources/channel#embed-object

    #### Status codes
    - 201: returned on success
    - 400: if one of the given fields is invalid

    ### PUT /bot/tags/<title:str>
    Update the tag with the given `title`.

    #### Request body
    >>> {
    ...     'title': str,
    ...     'embed': dict
    ... }

    The embed structure is the same as the embed structure that the Discord API
    expects. You can view the documentation for it here:
        https://discordapp.com/developers/docs/resources/channel#embed-object

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the tag with the given `title` could not be found

    ### PATCH /bot/tags/<title:str>
    Update the tag with the given `title`.

    #### Request body
    >>> {
    ...     'title': str,
    ...     'embed': dict
    ... }

    The embed structure is the same as the embed structure that the Discord API
    expects. You can view the documentation for it here:
        https://discordapp.com/developers/docs/resources/channel#embed-object

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the tag with the given `title` could not be found

    ### DELETE /bot/tags/<title:str>
    Deletes the tag with the given `title`.

    #### Status codes
    - 204: returned on success
    - 404: if a tag with the given `title` does not exist
    """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
