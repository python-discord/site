from django.contrib import admin

from .models import (
    BotSetting, DeletedMessage,
    DocumentationLink, Infraction,
    MessageDeletionContext, OffTopicChannelName,
    Role, Tag, User
)


admin.site.register(BotSetting)
admin.site.register(DeletedMessage)
admin.site.register(DocumentationLink)
admin.site.register(Infraction)
admin.site.register(MessageDeletionContext)
admin.site.register(OffTopicChannelName)
admin.site.register(Role)
admin.site.register(Tag)
admin.site.register(User)
