from django.db import migrations


def feature_selected(apps, schema_editor):
    Business = apps.get_model("directory", "Business")
    selected = ["the-remote-escape", "corralejo-info", "coworking-punto"]
    Business.objects.exclude(slug__in=selected).update(featured=False)
    Business.objects.filter(slug__in=selected).update(featured=True, partner=True)


class Migration(migrations.Migration):
    dependencies = [("directory", "0016_move_portals_to_businesses")]
    operations = [migrations.RunPython(feature_selected, migrations.RunPython.noop)]
