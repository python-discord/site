# Modified migration file to migrate existing filters to the new one

import django.contrib.postgres.fields
from django.apps.registry import Apps
from django.db import migrations, models
import django.db.models.deletion
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

import pydis_site.apps.api.models.bot.filters

OLD_LIST_NAMES = (('GUILD_INVITE', 'ALLOW'), ('FILE_FORMAT', 'DENY'), ('DOMAIN_NAME', 'DENY'), ('FILTER_TOKEN', 'DENY'))


def forward(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    filter_: pydis_site.apps.api.models.Filter = apps.get_model("api", "Filter")
    filter_list: pydis_site.apps.api.models.FilterList = apps.get_model("api", "FilterList")
    channel_range: pydis_site.apps.api.models.ChannelRange = apps.get_model("api", "ChannelRange")
    filter_action: pydis_site.apps.api.models.FilterAction = apps.get_model("api", "FilterAction")
    filter_list_old = apps.get_model("api", "FilterListOld")

    for name, type_ in OLD_LIST_NAMES:
        objects = filter_list_old.objects.filter(type=name)

        list_ = filter_list.objects.create(
            name=name.lower(),
            list_type=1 if type_ == "ALLOW" else 0,
            ping_type=["onduty"],
            filter_dm=True,
            dm_ping_type=["onduty"],
            delete_messages=True,
            bypass_roles=[267630620367257601],
            enabled=False,
            dm_content=None,
            infraction_type=None,
            infraction_reason="",
            infraction_duration=None,
            disallowed_channels=[],
            disallowed_categories=[],
            allowed_channels=[],
            allowed_categories=[]
        )

        for object_ in objects:
            new_object = filter_.objects.create(
                content=object_.content,
                filter_list=list_,
                description=object_.comment or "<no description provided>",
                additional_field=None,
                ping_type=None,
                filter_dm=None,
                dm_ping_type=None,
                delete_messages=None,
                bypass_roles=None,
                enabled=None,
                dm_content=None,
                infraction_type=None,
                infraction_reason="",
                infraction_duration=None,
                disallowed_channels=[],
                disallowed_categories=[],
                allowed_channels=[],
                allowed_categories=[]
            )
            new_object.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0069_documentationlink_validators'),
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
                ('description', models.CharField(help_text='Why this filter has been added.', max_length=200)),
                ('additional_field', models.BooleanField(help_text='Implementation specific field.', null=True)),
                ('ping_type', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), help_text='Who to ping when this filter triggers.', size=None, validators=[pydis_site.apps.api.models.bot.filters.validate_ping_field], null=True)),
                ('filter_dm', models.BooleanField(help_text='Whether DMs should be filtered.', null=True)),
                ('dm_ping_type', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), help_text='Who to ping when this filter triggers on a DM.', size=None, validators=[pydis_site.apps.api.models.bot.filters.validate_ping_field], null=True)),
                ('delete_messages', models.BooleanField(help_text='Whether this filter should delete messages triggering it.', null=True)),
                ('bypass_roles', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), help_text='Roles and users who can bypass this filter.', size=None, null=True)),
                ('enabled', models.BooleanField(help_text='Whether this filter is currently enabled.', null=True)),
                ('dm_content', models.CharField(help_text='The DM to send to a user triggering this filter.', max_length=1000, null=True)),
                ('infraction_type', models.CharField(choices=[('Note', 'Note'), ('Warn', 'Warn'), ('Mute', 'Mute'), ('Kick', 'Kick'), ('Ban', 'Ban')], help_text='The infraction to apply to this user.', max_length=4, null=True)),
                ('infraction_reason', models.CharField(help_text='The reason to give for the infraction.', max_length=1000)),
                ('infraction_duration', models.DurationField(help_text='The duration of the infraction. Null if permanent.', null=True)),
                ('disallowed_channels', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('disallowed_categories', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('allowed_channels', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('allowed_categories', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='FilterList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The unique name of this list.', max_length=50)),
                ('list_type', models.IntegerField(choices=[(1, 'Allow'), (0, 'Deny')], help_text='Whether this list is an allowlist or denylist')),
                ('ping_type', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), help_text='Who to ping when this filter triggers.', size=None, validators=[pydis_site.apps.api.models.bot.filters.validate_ping_field])),
                ('filter_dm', models.BooleanField(help_text='Whether DMs should be filtered.')),
                ('dm_ping_type', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), help_text='Who to ping when this filter triggers on a DM.', size=None, validators=[pydis_site.apps.api.models.bot.filters.validate_ping_field])),
                ('delete_messages', models.BooleanField(help_text='Whether this filter should delete messages triggering it.')),
                ('bypass_roles', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), help_text='Roles and users who can bypass this filter.', size=None)),
                ('enabled', models.BooleanField(help_text='Whether this filter is currently enabled.')),
                ('dm_content', models.CharField(help_text='The DM to send to a user triggering this filter.', max_length=1000, null=True)),
                ('infraction_type', models.CharField(choices=[('Note', 'Note'), ('Warn', 'Warn'), ('Mute', 'Mute'), ('Kick', 'Kick'), ('Ban', 'Ban')], help_text='The infraction to apply to this user.', max_length=4, null=True)),
                ('infraction_reason', models.CharField(help_text='The reason to give for the infraction.', max_length=1000)),
                ('infraction_duration', models.DurationField(help_text='The duration of the infraction. Null if permanent.', null=True)),
                ('disallowed_channels', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('disallowed_categories', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('allowed_channels', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('allowed_categories', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
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
