from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0088_new_filter_schema'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE api_filter "
            "ADD CONSTRAINT unique_filters UNIQUE NULLS NOT DISTINCT "
            "(content, additional_field, filter_list_id, dm_content, dm_embed, infraction_type, infraction_reason, infraction_duration, infraction_channel, guild_pings, filter_dm, dm_pings, remove_context, bypass_roles, enabled, send_alert, enabled_channels, disabled_channels, enabled_categories, disabled_categories)",
            reverse_sql="ALTER TABLE api_filter DROP CONSTRAINT unique_filters",
            state_operations=[
                migrations.AddConstraint(
                    model_name='filter',
                    constraint=models.UniqueConstraint(
                        fields=('content', 'additional_field', 'filter_list', 'dm_content', 'dm_embed', 'infraction_type', 'infraction_reason', 'infraction_duration', 'infraction_channel', 'guild_pings', 'filter_dm', 'dm_pings', 'remove_context', 'bypass_roles', 'enabled', 'send_alert', 'enabled_channels', 'disabled_channels', 'enabled_categories', 'disabled_categories'),
                        name='unique_filters'
                    ),
                ),
            ],
        ),
    ]
