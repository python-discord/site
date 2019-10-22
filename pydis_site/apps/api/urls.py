from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HealthcheckView, RulesView
from .viewsets import (
    BotSettingViewSet, DeletedMessageViewSet,
    DocumentationLinkViewSet, InfractionViewSet,
    LogEntryViewSet, NominationViewSet,
    OffTopicChannelNameViewSet,
    OffensiveMessageViewSet, ReminderViewSet,
    RoleViewSet, TagViewSet, UserViewSet
)


# http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
bot_router = DefaultRouter(trailing_slash=False)
bot_router.register(
    'bot-settings',
    BotSettingViewSet
)
bot_router.register(
    'deleted-messages',
    DeletedMessageViewSet
)
bot_router.register(
    'documentation-links',
    DocumentationLinkViewSet
)
bot_router.register(
    'infractions',
    InfractionViewSet
)
bot_router.register(
    'nominations',
    NominationViewSet
)
bot_router.register(
    'offensive-message',
    OffensiveMessageViewSet
)
bot_router.register(
    'off-topic-channel-names',
    OffTopicChannelNameViewSet,
    base_name='offtopicchannelname'
)
bot_router.register(
    'reminders',
    ReminderViewSet
)
bot_router.register(
    'roles',
    RoleViewSet
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
    path('bot/', include((bot_router.urls, 'api'), namespace='bot')),
    path('logs', LogEntryViewSet.as_view({'post': 'create'}), name='logs'),
    path('healthcheck', HealthcheckView.as_view(), name='healthcheck'),
    path('rules', RulesView.as_view(), name='rules')
)
