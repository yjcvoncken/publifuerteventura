from django.db import migrations, models


def migrate_plans(apps, schema_editor):
    Application = apps.get_model("directory", "CommunityApplication")
    Application.objects.filter(plan="advanced").update(plan="custom")
    Application.objects.filter(plan="basic").update(plan="advanced")
    Application.objects.filter(plan="personal").update(plan="basic")


class Migration(migrations.Migration):
    dependencies = [("directory", "0008_advanced_plan")]
    operations = [
        migrations.RunPython(migrate_plans, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="communityapplication",
            name="plan",
            field=models.CharField(choices=[("basic", "Basic — €100/year"), ("advanced", "Advanced — €250/year"), ("custom", "Custom — from €300/year")], default="basic", max_length=12),
        ),
    ]
