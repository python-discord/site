# Generated by Django 5.0 on 2023-12-17 13:31

import django.db.models.deletion
import pydis_site.apps.api.models.mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0092_remove_redirect_filter_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A short identifier for the mailing list.', max_length=50, unique=True)),
            ],
            bases=(pydis_site.apps.api.models.mixins.ModelReprMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MailingListSeenItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(help_text='A hash, or similar identifier, of the content that was seen.', max_length=100)),
                ('list', models.ForeignKey(help_text='The mailing list from which this seen item originates.', on_delete=django.db.models.deletion.CASCADE, related_name='seen_items', to='api.mailinglist')),
            ],
            bases=(pydis_site.apps.api.models.mixins.ModelReprMixin, models.Model),
        ),
        migrations.AddConstraint(
            model_name='mailinglistseenitem',
            constraint=models.UniqueConstraint(fields=('list', 'hash'), name='unique_list_and_hash'),
        ),
    ]
