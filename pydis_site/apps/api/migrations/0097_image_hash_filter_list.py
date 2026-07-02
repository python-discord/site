from datetime import timedelta

from django.apps.registry import Apps
from django.db import migrations

import pydis_site.apps.api.models.bot.filters


def create_image_hash_list(apps: Apps, _):
    """Create the 'image_hash' FilterList and remove legacy unique image filters."""
    filter_list: pydis_site.apps.api.models.FilterList = apps.get_model("api", "FilterList")
    filter_: pydis_site.apps.api.models.Filter = apps.get_model("api", "Filter")

    unique_list = filter_list.objects.filter(name="unique", list_type=0).first()
    if unique_list:
        filter_.objects.filter(filter_list=unique_list, content="image").delete()

    filter_list.objects.get_or_create(
        name="image_hash",
        list_type=0,
        defaults={
            "guild_pings": [],
            "filter_dm": True,
            "dm_pings": [],
            "remove_context": False,
            "bypass_roles": [],
            "enabled": True,
            "dm_content": "",
            "dm_embed": "",
            "infraction_type": "NONE",
            "infraction_reason": "",
            "infraction_duration": timedelta(seconds=0),
            "infraction_channel": 0,
            "disabled_channels": [],
            "disabled_categories": [],
            "enabled_channels": [],
            "enabled_categories": [],
            "send_alert": True,
        }
    )


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0096_merge_0093_user_alts_0095_user_display_name"),
    ]

    operations = [
        migrations.RunPython(
            code=create_image_hash_list,
            reverse_code=None
        ),
    ]
