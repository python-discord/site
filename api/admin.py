from django.contrib import admin

from .models import (
    DocumentationLink, Member,
    OffTopicChannelName, Role,
    SnakeName
)


admin.site.register(DocumentationLink)
admin.site.register(Member)
admin.site.register(OffTopicChannelName)
admin.site.register(Role)
admin.site.register(SnakeName)
