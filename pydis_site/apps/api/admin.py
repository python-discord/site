from django.contrib import admin

from .models import (
    BotSetting,
    DeletedMessage,
    DocumentationLink,
    Infraction,
    LogEntry,
    MessageDeletionContext,
    Nomination,
    OffTopicChannelName,
    Role,
    Tag,
    User
)


class LogEntryAdmin(admin.ModelAdmin):
    """Allows viewing logs in the Django Admin without allowing edits."""

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


admin.site.register(BotSetting)
admin.site.register(DeletedMessage)
admin.site.register(DocumentationLink)
admin.site.register(Infraction)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(MessageDeletionContext)
admin.site.register(Nomination)
admin.site.register(OffTopicChannelName)
admin.site.register(Role)
admin.site.register(Tag)
admin.site.register(User)
