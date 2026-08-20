from django.db import migrations


def add_branding(apps, schema_editor):
    apps.get_model("directory", "ShowcaseCard").objects.filter(title="The Remote Escape").update(
        destination_url="https://theremoteescape.com/",
        image_url="/static/img/theremoteescape-mark.svg",
        short_text="Find paid short-term work for your next stay in Spain.",
    )


def remove_branding(apps, schema_editor):
    apps.get_model("directory", "ShowcaseCard").objects.filter(title="The Remote Escape").update(
        destination_url="", image_url=""
    )


class Migration(migrations.Migration):
    dependencies = [("directory", "0013_alter_showcasecard_destination_url")]
    operations = [migrations.RunPython(add_branding, remove_branding)]
