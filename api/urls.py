from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .viewsets import SnakeNameViewSet


# http://www.django-rest-framework.org/api-guide/routers/#simplerouter
bot_router = SimpleRouter(trailing_slash=False)
bot_router.register(r'snake-names', SnakeNameViewSet, base_name='snakename')

app_name = 'api'
urlpatterns = (
    # Build URLs using something like...
    #
    # from django_hosts.resolvers import reverse
    # snake_name_endpoint = reverse('bot:snakename-list', host='api')  # `bot/` endpoints
    path('bot/', include((bot_router.urls, 'api'), namespace='bot')),
)
