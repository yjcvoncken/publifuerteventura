from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("directory", "0023_analyticspageview")]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="hero_image_content_type",
            field=models.CharField(blank=True, editable=False, max_length=100),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="hero_image_data",
            field=models.BinaryField(blank=True, editable=False, null=True),
        ),
    ]
