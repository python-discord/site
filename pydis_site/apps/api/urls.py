from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    GitHubArtifactsView,
    GitHubWebhookFilterView,
    HealthcheckView,
    RulesView,
)
from .viewsets import (
    AocAccountLinkViewSet,
    AocCompletionistBlockViewSet,
    BotSettingViewSet,
    BumpedThreadViewSet,
    DeletedMessageViewSet,
    DocumentationLinkViewSet,
    FilterListViewSet,
    FilterViewSet,
    InfractionViewSet,
    MailingListViewSet,
    NominationViewSet,
    OffTopicChannelNameViewSet,
    OffensiveMessageViewSet,
    ReminderViewSet,
    RoleViewSet,
    UserViewSet
)

# https://www.django-rest-framework.org/api-guide/routers/#defaultrouter
bot_router = DefaultRouter(trailing_slash=False)
# XXX: We should probably figure out why we have this registered twice.
bot_router.register(
    'filter/filter_lists',
    FilterListViewSet,
    basename="filter-filterlists-list",
)
bot_router.register(
    "aoc-account-links",
    AocAccountLinkViewSet
)
bot_router.register(
    "aoc-completionist-blocks",
    AocCompletionistBlockViewSet
)
bot_router.register(
    'filter/filters',
    FilterViewSet
)
bot_router.register(
    'bot-settings',
    BotSettingViewSet
)
bot_router.register(
    'bumped-threads',
    BumpedThreadViewSet
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
    'filter-lists',
    FilterListViewSet,
)
bot_router.register(
    'infractions',
    InfractionViewSet
)
bot_router.register(
    'mailing-lists',
    MailingListViewSet
)
bot_router.register(
    'nominations',
    NominationViewSet
)
bot_router.register(
    'offensive-messages',
    OffensiveMessageViewSet
)
bot_router.register(
    'off-topic-channel-names',
    OffTopicChannelNameViewSet,
    basename='offtopicchannelname'
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
    'users',
    UserViewSet
)

app_name = 'api'
urlpatterns = (
    # Build URLs using something like...
    #
    # from django_hosts.resolvers import reverse
    path('bot/', include((bot_router.urls, 'api'), namespace='bot')),
    path('healthcheck', HealthcheckView.as_view(), name='healthcheck'),
    path('rules', RulesView.as_view(), name='rules'),
    path(
        'github/artifact/<str:owner>/<str:repo>/<str:sha>/<str:action_name>/<str:artifact_name>',
        GitHubArtifactsView.as_view(),
        name="github-artifacts"
    ),
    path(
        'github/webhook-filter/<str:webhook_id>/<str:webhook_token>',
        GitHubWebhookFilterView.as_view(),
        name='github-webhook-filter'
    ),
)
