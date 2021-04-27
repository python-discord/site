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
    filter_settings: pydis_site.apps.api.models.FilterSettings = apps.get_model("api", "FilterSettings")
    channel_range: pydis_site.apps.api.models.ChannelRange = apps.get_model("api", "ChannelRange")
    filter_action: pydis_site.apps.api.models.FilterAction = apps.get_model("api", "FilterAction")
    filter_list_old = apps.get_model("api", "FilterListOld")

    for name, type_ in OLD_LIST_NAMES:
        objects = filter_list_old.objects.filter(type=name)

        default_action = filter_action.objects.create(
            user_dm=None,
            infraction_type=None,
            infraction_reason="",
            infraction_duration=None
        )
        default_action.save()
        default_range = channel_range.objects.create(
            disallowed_channels=[],
            disallowed_categories=[],
            allowed_channels=[],
            allowed_categories=[],
            default=True
        )
        default_range.save()
        default_settings = filter_settings.objects.create(
            ping_type=["onduty"],
            filter_dm=True,
            dm_ping_type=["onduty"],
            delete_messages=True,
            bypass_roles=[267630620367257601],
            enabled=False,
            default_action=default_action,
            default_range=default_range
        )
        default_settings.save()
        list_ = filter_list.objects.create(
            name=name.lower(),
            default_settings=default_settings,
            list_type=1 if type_ == "ALLOW" else 0
        )

        new_objects = []
        for object_ in objects:
            new_object = filter_.objects.create(
                content=object_.content,
                description=object_.comment or "<no description provided>",
                additional_field=None, override=None
            )
            new_object.save()
            new_objects.append(new_object)

        list_.filters.add(*new_objects)


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
            name='ChannelRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disallowed_channels', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('disallowed_categories', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('allowed_channels', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('allowed_categories', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('default', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(help_text='The definition of this filter.', max_length=100)),
                ('description', models.CharField(help_text='Why this filter has been added.', max_length=200)),
                ('additional_field', models.BooleanField(help_text='Implementation specific field.', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FilterAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_dm', models.CharField(help_text='The DM to send to a user triggering this filter.', max_length=1000, null=True)),
                ('infraction_type', models.CharField(choices=[('Note', 'Note'), ('Warn', 'Warn'), ('Mute', 'Mute'), ('Kick', 'Kick'), ('Ban', 'Ban')], help_text='The infraction to apply to this user.', max_length=4, null=True)),
                ('infraction_reason', models.CharField(help_text='The reason to give for the infraction.', max_length=1000)),
                ('infraction_duration', models.DurationField(help_text='The duration of the infraction. Null if permanent.', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FilterSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ping_type', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), help_text='Who to ping when this filter triggers.', size=None, validators=[pydis_site.apps.api.models.bot.filters.validate_ping_field])),
                ('filter_dm', models.BooleanField(help_text='Whenever DMs should be filtered.')),
                ('dm_ping_type', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), help_text='Who to ping when this filter triggers on a DM.', size=None, validators=[pydis_site.apps.api.models.bot.filters.validate_ping_field])),
                ('delete_messages', models.BooleanField(help_text='Whenever this filter should delete messages triggering it.')),
                ('bypass_roles', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), help_text='Roles and users who can bypass this filter.', size=None)),
                ('enabled', models.BooleanField(help_text='Whenever ths filter is currently enabled.')),
                ('default_action', models.ForeignKey(help_text='The default action to perform.', on_delete=django.db.models.deletion.CASCADE, to='api.FilterAction')),
                ('default_range', models.ForeignKey(help_text='Where does this filter apply.', on_delete=django.db.models.deletion.CASCADE, to='api.ChannelRange')),
            ],
        ),
        migrations.CreateModel(
            name='FilterOverride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ping_type', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), null=True, size=None, validators=[pydis_site.apps.api.models.bot.filters.validate_ping_field])),
                ('filter_dm', models.BooleanField(null=True)),
                ('dm_ping_type', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), null=True, size=None, validators=[pydis_site.apps.api.models.bot.filters.validate_ping_field])),
                ('delete_messages', models.BooleanField(null=True)),
                ('bypass_roles', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
                ('enabled', models.BooleanField(null=True)),
                ('filter_action', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.FilterAction')),
                ('filter_range', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.ChannelRange')),
            ],
        ),
        migrations.CreateModel(
            name='FilterList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The unique name of this list.', max_length=50)),
                ('list_type', models.IntegerField(choices=[], help_text='Whenever this list is an allowlist or denylist')),
                ('default_settings', models.ForeignKey(help_text='Default parameters of this list.', on_delete=django.db.models.deletion.CASCADE, to='api.FilterSettings')),
                ('filters', models.ManyToManyField(help_text='The content of this list.', to='api.Filter', default=[])),
            ],
        ),
        migrations.AddField(
            model_name='filter',
            name='override',
            field=models.ForeignKey(help_text='Override the default settings.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.FilterOverride'),
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
