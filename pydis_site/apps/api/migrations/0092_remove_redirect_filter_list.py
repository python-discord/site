from django.db import migrations
from django.apps.registry import Apps
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def forward(apps: Apps, _: BaseDatabaseSchemaEditor) -> None:
    apps.get_model("api", "FilterList").objects.filter(name="redirect").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0091_antispam_filter_list"),
    ]

    operations = [migrations.RunPython(forward, elidable=True)]
