# Generated by Django 3.1.14 on 2022-04-21 23:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0081_bumpedthread'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offtopicchannelname',
            name='name',
            field=models.CharField(help_text='The actual channel name that will be used on our Discord server.', max_length=96, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(regex="^[a-z0-9\\U0001d5a0-\\U0001d5b9-ǃ？’'＜＞⧹⧸]+$")]),
        ),
    ]
