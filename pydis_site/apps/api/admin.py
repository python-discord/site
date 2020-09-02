from typing import Optional

from django.contrib import admin
from django.http import HttpRequest

from .models import (
    BotSetting,
    DeletedMessage,
    DocumentationLink,
    Infraction,
    LogEntry,
    MessageDeletionContext,
    Nomination,
    OffTopicChannelName,
    OffensiveMessage,
    Role,
    User
)


class LogEntryAdmin(admin.ModelAdmin):
    """Allows viewing logs in the Django Admin without allowing edits."""

    actions = None
    list_display = ('timestamp', 'application', 'level', 'message')
    fieldsets = (
        ('Overview', {'fields': ('timestamp', 'application', 'logger_name')}),
        ('Metadata', {'fields': ('level', 'module', 'line')}),
        ('Contents', {'fields': ('message',)})
    )
    list_filter = ('application', 'level', 'timestamp')
    search_fields = ('message',)
    readonly_fields = (
        'application',
        'logger_name',
        'timestamp',
        'level',
        'module',
        'line',
        'message'
    )

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Deny manual LogEntry creation."""
        return False

    def has_delete_permission(
            self,
            request: HttpRequest,
            obj: Optional[LogEntry] = None
    ) -> bool:
        """Deny LogEntry deletion."""
        return False


admin.site.register(BotSetting)
admin.site.register(DeletedMessage)
admin.site.register(DocumentationLink)
admin.site.register(Infraction)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(MessageDeletionContext)
admin.site.register(Nomination)
admin.site.register(OffensiveMessage)
admin.site.register(OffTopicChannelName)
admin.site.register(Role)
admin.site.register(User)
