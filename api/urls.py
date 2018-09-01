from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import HealthcheckView
from .viewsets import DocumentationLinkViewSet, MemberViewSet, OffTopicChannelNameViewSet, SnakeNameViewSet


# http://www.django-rest-framework.org/api-guide/routers/#simplerouter
bot_router = SimpleRouter(trailing_slash=False)
bot_router.register('documentation-links', DocumentationLinkViewSet)
bot_router.register('off-topic-channel-names', OffTopicChannelNameViewSet, base_name='offtopicchannelname')
bot_router.register('members', MemberViewSet)
bot_router.register('snake-names', SnakeNameViewSet, base_name='snakename')


app_name = 'api'
urlpatterns = (
    # Build URLs using something like...
    #
    # from django_hosts.resolvers import reverse
    # snake_name_endpoint = reverse('bot:snakename-list', host='api')  # `bot/` endpoints
    path('bot/', include((bot_router.urls, 'api'), namespace='bot')),
    path('healthcheck', HealthcheckView.as_view(), name='healthcheck')
)
