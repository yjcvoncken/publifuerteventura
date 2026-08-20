from django.db import migrations


def seed_portals(apps, schema_editor):
    ShowcaseCard = apps.get_model("directory", "ShowcaseCard")
    portals = (
        ("The Remote Escape", "A different way to work, meet and experience Fuerteventura.", "", 10),
        ("Corralejo.info", "The complete local guide to Corralejo and Fuerteventura.", "https://www.corralejo.info/", 20),
        ("Coworking Punto", "A shared space for work, ideas and local connections.", "https://coworkingpunto.com/", 30),
    )
    for title, text, url, order in portals:
        ShowcaseCard.objects.get_or_create(title=title, defaults={"short_text": text, "destination_url": url, "order": order})


def unseed_portals(apps, schema_editor):
    apps.get_model("directory", "ShowcaseCard").objects.filter(title__in=[
        "The Remote Escape", "Corralejo.info", "Coworking Punto"
    ]).delete()


class Migration(migrations.Migration):
    dependencies = [("directory", "0011_seed_showcase_content")]
    operations = [migrations.RunPython(seed_portals, unseed_portals)]
