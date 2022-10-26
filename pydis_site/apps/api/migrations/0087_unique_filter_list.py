from datetime import timedelta

from django.apps.registry import Apps
from django.db import migrations

import pydis_site.apps.api.models.bot.filters


def create_unique_list(apps: Apps, _):
    """Create the 'unique' FilterList and its related Filters."""
    filter_list: pydis_site.apps.api.models.FilterList = apps.get_model("api", "FilterList")
    filter_: pydis_site.apps.api.models.Filter = apps.get_model("api", "Filter")

    list_ = filter_list.objects.create(
        name="unique",
        list_type=0,
        guild_pings=[],
        filter_dm=True,
        dm_pings=[],
        delete_messages=False,
        bypass_roles=[],
        enabled=True,
        dm_content="",
        dm_embed="",
        infraction_type="",
        infraction_reason="",
        infraction_duration=timedelta(seconds=0),
        infraction_channel=None,
        disabled_channels=[],
        disabled_categories=[],
        enabled_channels=[],
        enabled_categories=[],
        send_alert=True
    )

    everyone = filter_.objects.create(
        content="everyone",
        filter_list=list_,
        description="",
        delete_messages=True,
        bypass_roles=["Helpers"],
        dm_content=(
            "Please don't try to ping `@everyone` or `@here`. Your message has been removed. "
            "If you believe this was a mistake, please let staff know!"
        ),
    )
    everyone.save()

    webhook = filter_.objects.create(
        content="webhook",
        filter_list=list_,
        description="",
        delete_messages=True,
        dm_content=(
            "Looks like you posted a Discord webhook URL. "
            "Therefore, your message has been removed, and your webhook has been deleted. "
            "You can re-create it if you wish to. "
            "If you believe this was a mistake, please let us know."
        ),
    )
    webhook.save()

    rich_embed = filter_.objects.create(
        content="rich_embed",
        filter_list=list_,
        description="",
        guild_pings=["Moderators"],
        dm_pings=["Moderators"]
    )
    rich_embed.save()

    discord_token = filter_.objects.create(
        content="discord_token",
        filter_list=list_,
        filter_dm=False,
        delete_messages=True,
        dm_content=(
            "I noticed you posted a seemingly valid Discord API "
            "token in your message and have removed your message. "
            "This means that your token has been **compromised**. "
            "Please change your token **immediately** at: "
            "<https://discord.com/developers/applications>\n\n"
            "Feel free to re-post it with the token removed. "
            "If you believe this was a mistake, please let us know!"
        )
    )
    discord_token.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0086_unique_constraint_filters'),
    ]

    operations = [
        migrations.RunPython(
            code=create_unique_list,
            reverse_code=None
        ),
    ]