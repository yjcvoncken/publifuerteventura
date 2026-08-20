from django.db import migrations


def use_official_logos(apps, schema_editor):
    Business = apps.get_model("directory", "Business")
    logos = {
        "the-remote-escape": "https://theremoteescape.com/static/theremoteescape-mark.43f83534365d.svg",
        "corralejo-info": "https://www.corralejo.info/wp-content/uploads/2024/04/corralejo2-logo.png",
        "coworking-punto": "https://coworkingpunto.com/wp-content/uploads/2023/03/logoweb3.jpg",
    }
    for slug, image_url in logos.items():
        Business.objects.filter(slug=slug).update(image_url=image_url)


class Migration(migrations.Migration):
    dependencies = [("directory", "0018_sitesettings_team_eyebrow_sitesettings_team_intro_and_more")]
    operations = [migrations.RunPython(use_official_logos, migrations.RunPython.noop)]
