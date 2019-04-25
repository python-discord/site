import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_create_table_log_entry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nomination',
            name='user',
            field=models.ForeignKey(help_text='The nominated user.', on_delete=django.db.models.deletion.CASCADE, related_name='nomination', to='api.User'),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='author',
            field=models.ForeignKey(help_text='The staff member that nominated this user.', on_delete=django.db.models.deletion.CASCADE, related_name='nomination_set', to='api.User'),
        ),
        migrations.RenameField(
            model_name='nomination',
            old_name='author',
            new_name='actor',
        ),
        migrations.AddField(
            model_name='nomination',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='nomination',
            name='unnominate_reason',
            field=models.TextField(default='', help_text='Why the nomination was ended.'),
        ),
        migrations.AddField(
            model_name='nomination',
            name='unwatched_at',
            field=models.DateTimeField(help_text='When the nomination was ended.', null=True),
        ),
    ]
