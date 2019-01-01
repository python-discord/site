from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HealthcheckView
from .viewsets import (
    DocumentationLinkViewSet, InfractionViewSet,
    OffTopicChannelNameViewSet, RoleViewSet,
    SnakeFactViewSet, SnakeIdiomViewSet,
    SnakeNameViewSet, SpecialSnakeViewSet,
    TagViewSet, UserViewSet
)


# http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
bot_router = DefaultRouter(trailing_slash=False)
bot_router.register(
    'documentation-links',
    DocumentationLinkViewSet
)
bot_router.register(
    'infractions',
    InfractionViewSet
)
bot_router.register(
    'off-topic-channel-names',
    OffTopicChannelNameViewSet,
    base_name='offtopicchannelname'
)
bot_router.register(
    'roles',
    RoleViewSet
)
bot_router.register(
    'snake-facts',
    SnakeFactViewSet
)
bot_router.register(
    'snake-idioms',
    SnakeIdiomViewSet
)
bot_router.register(
    'snake-names',
    SnakeNameViewSet,
    base_name='snakename'
)
bot_router.register(
    'special-snakes',
    SpecialSnakeViewSet
)
bot_router.register(
    'tags',
    TagViewSet
)
bot_router.register(
    'users',
    UserViewSet
)

app_name = 'api'
urlpatterns = (
    # Build URLs using something like...
    #
    # from django_hosts.resolvers import reverse
    # snake_name_endpoint = reverse('bot:snakename-list', host='api')  # `bot/` endpoints
    path('bot/', include((bot_router.urls, 'api'), namespace='bot')),
    path('healthcheck', HealthcheckView.as_view(), name='healthcheck')
)
