from django.db import migrations, models


def preserve_existing_homepage_pattern(apps, schema_editor):
    Business = apps.get_model("directory", "Business")
    featured = Business.objects.filter(featured=True, partner=True).order_by("pk")
    for position, business in enumerate(featured, start=1):
        business.homepage_size = 1 if position == 1 or position % 5 == 0 else 2
        business.save(update_fields=("homepage_size",))


class Migration(migrations.Migration):
    dependencies = [("directory", "0027_rename_sponsor_logo_fields")]

    operations = [
        migrations.AddField(
            model_name="business",
            name="homepage_size",
            field=models.PositiveSmallIntegerField(
                choices=[(1, "1 — Large"), (2, "2 — Small")],
                default=2,
                help_text="Choose 1 for a large homepage card or 2 for a small card.",
            ),
        ),
        migrations.RunPython(preserve_existing_homepage_pattern, migrations.RunPython.noop),
    ]
