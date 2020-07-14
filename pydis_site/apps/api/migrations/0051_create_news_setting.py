from django.db import migrations


def up(apps, schema_editor):
    BotSetting = apps.get_model('api', 'BotSetting')
    setting = BotSetting(
        name='news',
        data={}
    ).save()


def down(apps, schema_editor):
    BotSetting = apps.get_model('api', 'BotSetting')
    BotSetting.objects.get(name='news').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_remove_infractions_active_default_value'),
    ]

    operations = [
        migrations.RunPython(up, down)
    ]
