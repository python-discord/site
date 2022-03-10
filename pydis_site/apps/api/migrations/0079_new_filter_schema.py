# Modified migration file to migrate existing filters to the new one
from datetime import timedelta

import django.contrib.postgres.fields
from django.apps.registry import Apps
from django.db import migrations, models
import django.db.models.deletion
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

import pydis_site.apps.api.models.bot.filters

OLD_LIST_NAMES = (('GUILD_INVITE', True), ('GUILD_INVITE', False), ('FILE_FORMAT', True), ('DOMAIN_NAME', False), ('FILTER_TOKEN', False), ('REDIRECT', False))
change_map = {
    "FILTER_TOKEN": "token",
    "DOMAIN_NAME": "domain",
    "GUILD_INVITE": "invite",
    "FILE_FORMAT": "extension",
    "REDIRECT": "redirect"
}


def forward(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    filter_: pydis_site.apps.api.models.Filter = apps.get_model("api", "Filter")
    filter_list: pydis_site.apps.api.models.FilterList = apps.get_model("api", "FilterList")
    filter_list_old = apps.get_model("api", "FilterListOld")

    for name, type_ in OLD_LIST_NAMES:
        objects = filter_list_old.objects.filter(type=name, allowed=type_)
        if name == "DOMAIN_NAME":
            dm_content = "Your message has been removed because it contained a blocked domain: `{domain}`."
        elif name == "GUILD_INVITE":
            dm_content = "Per Rule 6, your invite link has been removed. " \
                         "Our server rules can be found here: https://pythondiscord.com/pages/rules"
        else:
            dm_content = ""

        list_ = filter_list.objects.create(
            name=change_map[name],
            list_type=int(type_),
            guild_pings=(["Moderators"] if name != "FILE_FORMAT" else []),
            filter_dm=True,
            dm_pings=[],
            delete_messages=(True if name != "FILTER_TOKEN" else False),
            bypass_roles=["Helpers"],
            enabled=True,
            dm_content=dm_content,
            dm_embed="" if name != "FILE_FORMAT" else "*Defined at runtime.*",
            infraction_type="",
            infraction_reason="",
            infraction_duration=timedelta(seconds=0),
            disabled_channels=[],
            disabled_categories=(["CODE JAM"] if name in ("FILE_FORMAT", "GUILD_INVITE") else []),
            enabled_channels=[],
            send_alert=(name in ('GUILD_INVITE', 'DOMAIN_NAME', 'FILTER_TOKEN'))
        )

        for object_ in objects:
            new_object = filter_.objects.create(
                content=object_.content,
                filter_list=list_,
                description=object_.comment,
                additional_field=None,
                guild_pings=None,
                filter_dm=None,
                dm_pings=None,
                delete_messages=None,
                bypass_roles=None,
                enabled=None,
                dm_content=None,
                dm_embed=None,
                infraction_type=None,
                infraction_reason=None,
                infraction_duration=None,
                disabled_channels=None,
                disabled_categories=None,
                enabled_channels=None,
                send_alert=None,
            )
            new_object.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0078_merge_20211213_0552'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FilterList',
            new_name='FilterListOld'
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(help_text='The definition of this filter.', max_length=100)),
                ('description', models.CharField(help_text='Why this filter has been added.', max_length=200, null=True)),
                ('additional_field', django.contrib.postgres.fields.jsonb.JSONField(help_text='Implementation specific field.', null=True)),
                ('guild_pings', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), help_text='Who to ping when this filter triggers.', size=None, null=True)),
                ('filter_dm', models.BooleanField(help_text='Whether DMs should be filtered.', null=True)),
                ('dm_pings', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), help_text='Who to ping when this filter triggers on a DM.', size=None, null=True)),
                ('delete_messages', models.BooleanField(help_text='Whether this filter should delete messages triggering it.', null=True)),
                ('bypass_roles', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), help_text='Roles and users who can bypass this filter.', size=None, null=True)),
                ('enabled', models.BooleanField(help_text='Whether this filter is currently enabled.', null=True)),
                ('dm_content', models.CharField(help_text='The DM to send to a user triggering this filter.', max_length=1000, null=True)),
                ('dm_embed', models.CharField(help_text='The content of the DM embed', max_length=2000, null=True)),
                ('infraction_type', models.CharField(choices=[('note', 'Note'), ('warning', 'Warning'), ('watch', 'Watch'), ('mute', 'Mute'), ('kick', 'Kick'), ('ban', 'Ban'), ('superstar', 'Superstar'), ('voice_ban', 'Voice Ban')], help_text='The infraction to apply to this user.', max_length=9, null=True)),
                ('infraction_reason', models.CharField(help_text='The reason to give for the infraction.', max_length=1000, null=True)),
                ('infraction_duration', models.DurationField(help_text='The duration of the infraction. Null if permanent.', null=True)),
                ('disabled_channels', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), help_text="Channels in which to not run the filter.", null=True, size=None)),
                ('disabled_categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), help_text="Categories in which to not run the filter.", null=True, size=None)),
                ('enabled_channels', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), help_text="Channels in which to run the filter even if it's disabled in the category.", null=True, size=None)),
                ('send_alert', models.BooleanField(help_text='Whether an alert should be sent.', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FilterList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The unique name of this list.', max_length=50)),
                ('list_type', models.IntegerField(choices=[(1, 'Allow'), (0, 'Deny')], help_text='Whether this list is an allowlist or denylist')),
                ('guild_pings', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), help_text='Who to ping when this filter triggers.', size=None)),
                ('filter_dm', models.BooleanField(help_text='Whether DMs should be filtered.')),
                ('dm_pings', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), help_text='Who to ping when this filter triggers on a DM.', size=None)),
                ('delete_messages', models.BooleanField(help_text='Whether this filter should delete messages triggering it.')),
                ('bypass_roles', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), help_text='Roles and users who can bypass this filter.', size=None)),
                ('enabled', models.BooleanField(help_text='Whether this filter is currently enabled.')),
                ('dm_content', models.CharField(help_text='The DM to send to a user triggering this filter.', max_length=1000, null=True)),
                ('dm_embed', models.CharField(help_text='The content of the DM embed', max_length=2000, null=True)),
                ('infraction_type', models.CharField(choices=[('note', 'Note'), ('warning', 'Warning'), ('watch', 'Watch'), ('mute', 'Mute'), ('kick', 'Kick'), ('ban', 'Ban'), ('superstar', 'Superstar'), ('voice_ban', 'Voice Ban')], help_text='The infraction to apply to this user.', max_length=9, null=True)),
                ('infraction_reason', models.CharField(help_text='The reason to give for the infraction.', max_length=1000)),
                ('infraction_duration', models.DurationField(help_text='The duration of the infraction. Null if permanent.', null=True)),
                ('disabled_channels', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), help_text="Channels in which to not run the filter.", size=None)),
                ('disabled_categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), help_text="Categories in which to not run the filter.", size=None)),
                ('enabled_channels', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), help_text="Channels in which to run the filter even if it's disabled in the category.", size=None)),
                ('send_alert', models.BooleanField(help_text='Whether an alert should be sent.')),
            ],
        ),
        migrations.AddField(
            model_name='filter',
            name='filter_list',
            field=models.ForeignKey(help_text='The filter list containing this filter.', on_delete=django.db.models.deletion.CASCADE, related_name='filters', to='api.FilterList'),
        ),
        migrations.AddConstraint(
            model_name='filterlist',
            constraint=models.UniqueConstraint(fields=('name', 'list_type'), name='unique_name_type'),
        ),
        migrations.RunPython(
            code=forward,  # Core of the migration
            reverse_code=lambda *_: None
        ),
        migrations.DeleteModel(
            name='FilterListOld'
        )
    ]
