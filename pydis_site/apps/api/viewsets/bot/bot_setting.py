from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.bot.bot_setting import BotSetting
from pydis_site.apps.api.serializers import BotSettingSerializer


class BotSettingViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """View providing update operations on bot setting routes."""

    serializer_class = BotSettingSerializer
    queryset = BotSetting.objects.all()
