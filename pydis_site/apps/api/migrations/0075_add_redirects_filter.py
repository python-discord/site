# Generated by Django 3.0.14 on 2021-11-17 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0074_reminder_failures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filterlist',
            name='type',
            field=models.CharField(choices=[('GUILD_INVITE', 'Guild Invite'), ('FILE_FORMAT', 'File Format'), ('DOMAIN_NAME', 'Domain Name'), ('FILTER_TOKEN', 'Filter Token'), ('REDIRECT', 'Redirect')], help_text='The type of allowlist this is on.', max_length=50),
        ),
    ]
