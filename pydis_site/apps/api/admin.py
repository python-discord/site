from __future__ import annotations

import json
from typing import Iterable, Optional, Tuple

from django import urls
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import SafeString, format_html

from .models import (
    BotSetting,
    DeletedMessage,
    DocumentationLink,
    Infraction,
    MessageDeletionContext,
    Nomination,
    OffTopicChannelName,
    OffensiveMessage,
    Role,
    User
)

admin.site.site_header = "Python Discord | Administration"
admin.site.site_title = "Python Discord"


@admin.register(BotSetting)
class BotSettingAdmin(admin.ModelAdmin):
    """Admin formatting for the BotSetting model."""

    fields = ("name", "data")
    list_display = ("name",)
    readonly_fields = ("name",)

    def has_add_permission(self, *args) -> bool:
        """Prevent adding from django admin."""
        return False

    def has_delete_permission(self, *args) -> bool:
        """Prevent deleting from django admin."""
        return False


@admin.register(DocumentationLink)
class DocumentationLinkAdmin(admin.ModelAdmin):
    """Admin formatting for the DocumentationLink model."""

    fields = ("package", "base_url", "inventory_url")
    list_display = ("package", "base_url", "inventory_url")
    list_editable = ("base_url", "inventory_url")
    search_fields = ("package",)


class InfractionActorFilter(admin.SimpleListFilter):
    """Actor Filter for Infraction Admin list page."""

    title = "Actor"
    parameter_name = "actor"

    def lookups(self, request: HttpRequest, model: NominationAdmin) -> Iterable[Tuple[int, str]]:
        """Selectable values for viewer to filter by."""
        actor_ids = Infraction.objects.order_by().values_list("actor").distinct()
        actors = User.objects.filter(id__in=actor_ids)
        return ((a.id, a.username) for a in actors)

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> Optional[QuerySet]:
        """Query to filter the list of Users against."""
        if not self.value():
            return
        return queryset.filter(actor__id=self.value())


@admin.register(Infraction)
class InfractionAdmin(admin.ModelAdmin):
    """Admin formatting for the Infraction model."""

    fieldsets = (
        ("Members", {"fields": ("user", "actor")}),
        ("Action", {"fields": ("type", "hidden", "active")}),
        ("Dates", {"fields": ("inserted_at", "expires_at")}),
        ("Reason", {"fields": ("reason",)}),
    )
    readonly_fields = (
        "user",
        "actor",
        "type",
        "inserted_at",
        "expires_at",
        "active",
        "hidden"
    )
    list_display = (
        "type",
        "active",
        "user",
        "inserted_at",
        "reason",
    )
    search_fields = (
        "id",
        "user__name",
        "user__id",
        "actor__name",
        "actor__id",
        "reason",
        "type"
    )
    list_filter = (
        "type",
        "hidden",
        "active",
        InfractionActorFilter
    )

    def has_add_permission(self, *args) -> bool:
        """Prevent adding from django admin."""
        return False


@admin.register(DeletedMessage)
class DeletedMessageAdmin(admin.ModelAdmin):
    """Admin formatting for the DeletedMessage model."""

    fields = (
        "id",
        "author",
        "channel_id",
        "content",
        "embed_data",
        "context",
        "view_full_log"
    )

    exclude = ("embeds", "deletion_context")

    search_fields = (
        "id",
        "content",
        "author__name",
        "author__id",
        "deletion_context__actor__name",
        "deletion_context__actor__id"
    )

    list_display = ("id", "author", "channel_id")

    def embed_data(self, message: DeletedMessage) -> Optional[str]:
        """Format embed data in a code block for better readability."""
        if message.embeds:
            return format_html(
                "<pre style='word-wrap: break-word; white-space: pre-wrap; overflow-x: auto;'>"
                "<code>{0}</code></pre>",
                json.dumps(message.embeds, indent=4)
            )

    embed_data.short_description = "Embeds"

    @staticmethod
    def context(message: DeletedMessage) -> str:
        """Provide full context info with a link through to context admin view."""
        link = urls.reverse(
            "admin:api_messagedeletioncontext_change",
            args=[message.deletion_context.id]
        )
        details = (
            f"Deleted by {message.deletion_context.actor} at "
            f"{message.deletion_context.creation}"
        )
        return format_html("<a href='{0}'>{1}</a>", link, details)

    @staticmethod
    def view_full_log(message: DeletedMessage) -> str:
        """Provide a link to the message logs for the relevant context."""
        return format_html(
            "<a href='{0}'>Click to view full context log</a>",
            message.deletion_context.log_url
        )

    def has_add_permission(self, *args) -> bool:
        """Prevent adding from django admin."""
        return False

    def has_change_permission(self, *args) -> bool:
        """Prevent editing from django admin."""
        return False


class DeletedMessageInline(admin.TabularInline):
    """Tabular Inline Admin model for Deleted Message to be viewed within Context."""

    model = DeletedMessage


@admin.register(MessageDeletionContext)
class MessageDeletionContextAdmin(admin.ModelAdmin):
    """Admin formatting for the MessageDeletionContext model."""

    fields = ("actor", "creation")
    list_display = ("id", "creation", "actor")
    inlines = (DeletedMessageInline,)

    def has_add_permission(self, *args) -> bool:
        """Prevent adding from django admin."""
        return False

    def has_change_permission(self, *args) -> bool:
        """Prevent editing from django admin."""
        return False


class NominationActorFilter(admin.SimpleListFilter):
    """Actor Filter for Nomination Admin list page."""

    title = "Actor"
    parameter_name = "actor"

    def lookups(self, request: HttpRequest, model: NominationAdmin) -> Iterable[Tuple[int, str]]:
        """Selectable values for viewer to filter by."""
        actor_ids = Nomination.objects.order_by().values_list("actor").distinct()
        actors = User.objects.filter(id__in=actor_ids)
        return ((a.id, a.username) for a in actors)

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> Optional[QuerySet]:
        """Query to filter the list of Users against."""
        if not self.value():
            return
        return queryset.filter(actor__id=self.value())


@admin.register(Nomination)
class NominationAdmin(admin.ModelAdmin):
    """Admin formatting for the Nomination model."""

    search_fields = (
        "user__name",
        "user__id",
        "actor__name",
        "actor__id",
        "reason",
        "end_reason"
    )

    list_filter = ("active", NominationActorFilter)

    list_display = (
        "user",
        "active",
        "reason",
        "actor",
    )

    fields = (
        "user",
        "active",
        "actor",
        "reason",
        "inserted_at",
        "ended_at",
        "end_reason"
    )

    # only allow reason fields to be edited.
    readonly_fields = (
        "user",
        "active",
        "actor",
        "inserted_at",
        "ended_at"
    )

    def has_add_permission(self, *args) -> bool:
        """Prevent adding from django admin."""
        return False


@admin.register(OffTopicChannelName)
class OffTopicChannelNameAdmin(admin.ModelAdmin):
    """Admin formatting for the OffTopicChannelName model."""

    search_fields = ("name",)
    list_filter = ("used",)


@admin.register(OffensiveMessage)
class OffensiveMessageAdmin(admin.ModelAdmin):
    """Admin formatting for the OffensiveMessage model."""

    def message_jumplink(self, message: OffensiveMessage) -> SafeString:
        """Message ID hyperlinked to the direct discord jumplink."""
        return format_html(
            '<a href="https://canary.discordapp.com/channels/267624335836053506/{0}/{1}">{1}</a>',
            message.channel_id,
            message.id
        )

    message_jumplink.short_description = "Message ID"

    search_fields = ("id", "channel_id")
    list_display = ("id", "channel_id", "delete_date")
    fields = ("message_jumplink", "channel_id", "delete_date")
    readonly_fields = ("message_jumplink", "channel_id")

    def has_add_permission(self, *args) -> bool:
        """Prevent adding from django admin."""
        return False


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin formatting for the Role model."""

    def coloured_name(self, role: Role) -> SafeString:
        """Role name with html style colouring."""
        return format_html(
            '<span style="color: {0}!important; font-weight: bold;">{1}</span>',
            f"#{role.colour:06X}",
            role.name
        )

    coloured_name.short_description = "Name"

    def colour_with_preview(self, role: Role) -> SafeString:
        """Show colour value in both int and hex, in bolded and coloured style."""
        return format_html(
            "<span style='color: {0}; font-weight: bold;'>{0} ({1})</span>",
            f"#{role.colour:06x}",
            role.colour
        )

    colour_with_preview.short_description = "Colour"

    def permissions_with_calc_link(self, role: Role) -> SafeString:
        """Show permissions with link to API permissions calculator page."""
        return format_html(
            "<a href='https://discordapi.com/permissions.html#{0}' target='_blank'>{0}</a>",
            role.permissions
        )

    permissions_with_calc_link.short_description = "Permissions"

    search_fields = ("name", "id")
    list_display = ("coloured_name",)
    fields = ("id", "name", "colour_with_preview", "permissions_with_calc_link", "position")

    def has_add_permission(self, *args) -> bool:
        """Prevent adding from django admin."""
        return False

    def has_change_permission(self, *args) -> bool:
        """Prevent editing from django admin."""
        return False


class UserRoleFilter(admin.SimpleListFilter):
    """List Filter for User list Admin page."""

    title = "Role"
    parameter_name = "role"

    def lookups(self, request: HttpRequest, model: UserAdmin) -> Iterable[Tuple[str, str]]:
        """Selectable values for viewer to filter by."""
        roles = Role.objects.all()
        return ((r.name, r.name) for r in roles)

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> Optional[QuerySet]:
        """Query to filter the list of Users against."""
        if not self.value():
            return
        role = Role.objects.get(name=self.value())
        return queryset.filter(roles__contains=[role.id])


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin formatting for the User model."""

    def top_role_coloured(self, user: User) -> SafeString:
        """Returns the top role of the user with html style matching role colour."""
        return format_html(
            '<span style="color: {0}; font-weight: bold;">{1}</span>',
            f"#{user.top_role.colour:06X}",
            user.top_role.name
        )

    top_role_coloured.short_description = "Top Role"

    def all_roles_coloured(self, user: User) -> SafeString:
        """Returns all user roles with html style matching role colours."""
        roles = Role.objects.filter(id__in=user.roles)
        return format_html(
            "</br>".join(
                f'<span style="color: #{r.colour:06X}; font-weight: bold;">{r.name}</span>'
                for r in roles
            )
        )

    all_roles_coloured.short_description = "All Roles"

    search_fields = ("name", "id", "roles")
    list_filter = (UserRoleFilter, "in_guild")
    list_display = ("username", "top_role_coloured", "in_guild")
    fields = ("username", "id", "in_guild", "all_roles_coloured")
    sortable_by = ("username",)

    def has_add_permission(self, *args) -> bool:
        """Prevent adding from django admin."""
        return False

    def has_change_permission(self, *args) -> bool:
        """Prevent editing from django admin."""
        return False
