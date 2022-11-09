from datetime import timedelta

from django.apps.registry import Apps
from django.db import migrations

import pydis_site.apps.api.models.bot.filters


def create_antispam_list(apps: Apps, _):
    """Create the 'unique' FilterList and its related Filters."""
    filter_list: pydis_site.apps.api.models.FilterList = apps.get_model("api", "FilterList")
    filter_: pydis_site.apps.api.models.Filter = apps.get_model("api", "Filter")

    list_ = filter_list.objects.create(
        name="antispam",
        list_type=0,
        guild_pings=["Moderators"],
        filter_dm=False,
        dm_pings=[],
        remove_context=True,
        bypass_roles=["Helpers"],
        enabled=True,
        dm_content="",
        dm_embed="",
        infraction_type="MUTE",
        infraction_reason="",
        infraction_duration=timedelta(seconds=600),
        infraction_channel=0,
        disabled_channels=[],
        disabled_categories=["CODE JAM"],
        enabled_channels=[],
        enabled_categories=[],
        send_alert=True
    )

    rules = ("duplicates", "attachments", "burst", "chars", "emoji", "links", "mentions", "newlines", "role_mentions")

    filter_.objects.bulk_create([filter_(content=rule, filter_list=list_) for rule in rules])


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0087_unique_filter_list'),
    ]

    operations = [
        migrations.RunPython(
            code=create_antispam_list,
            reverse_code=None
        ),
    ]
