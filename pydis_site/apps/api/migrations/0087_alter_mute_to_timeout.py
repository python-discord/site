from django.apps.registry import Apps
from django.db import migrations, models

import pydis_site.apps.api.models


def rename_type(apps: Apps, _) -> None:
    infractions: pydis_site.apps.api.models.Infraction = apps.get_model("api", "Infraction")
    infractions.objects.filter(type="mute").update(type="timeout")


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0086_infraction_jump_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infraction',
            name='type',
            field=models.CharField(choices=[('note', 'Note'), ('warning', 'Warning'), ('watch', 'Watch'), ('timeout', 'Timeout'), ('kick', 'Kick'), ('ban', 'Ban'), ('superstar', 'Superstar'), ('voice_ban', 'Voice Ban'), ('voice_mute', 'Voice Mute')], help_text='The type of the infraction.', max_length=10),
        ),
        migrations.RunPython(rename_type, migrations.RunPython.noop)
    ]
