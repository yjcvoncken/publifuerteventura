from django.db import migrations


def seed_showcase(apps, schema_editor):
    SiteSettings = apps.get_model("directory", "SiteSettings")
    Sponsor = apps.get_model("directory", "Sponsor")
    TeamMember = apps.get_model("directory", "TeamMember")

    SiteSettings.objects.get_or_create(pk=1)
    people = (
        ("ChanTaL MonTaLdo", "Creator, initiator and Project Manager", 10),
        ("Ángela Pascuali", "Producer, writer and director", 20),
        ("Yannick", "Web development and technology", 30),
        ("coworking.com", "Coworking and networking reference point", 40),
        ("Corralejo.info", "Sponsor", 50),
    )
    for name, role, order in people:
        TeamMember.objects.get_or_create(name=name, defaults={"role": role, "order": order})
    Sponsor.objects.get_or_create(name="Corralejo.info", defaults={"order": 10})


def unseed_showcase(apps, schema_editor):
    apps.get_model("directory", "TeamMember").objects.filter(
        name__in=["ChanTaL MonTaLdo", "Ángela Pascuali", "Yannick", "coworking.com", "Corralejo.info"]
    ).delete()
    apps.get_model("directory", "Sponsor").objects.filter(name="Corralejo.info").delete()


class Migration(migrations.Migration):
    dependencies = [("directory", "0010_showcasecard_sitesettings_sponsor_teammember")]
    operations = [migrations.RunPython(seed_showcase, unseed_showcase)]
