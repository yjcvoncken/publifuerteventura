from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("directory", "0024_sitesettings_database_hero")]

    operations = [
        migrations.AddField(model_name="sponsor", name="cover_image", field=models.FileField(blank=True, upload_to="collaborations/covers/")),
        migrations.AddField(model_name="sponsor", name="cover_image_url", field=models.URLField(blank=True, help_text="Optional external cover photograph URL.")),
        migrations.AlterField(model_name="sponsor", name="image", field=models.FileField(blank=True, upload_to="showcase/sponsors/", verbose_name="logo")),
        migrations.AlterField(model_name="sponsor", name="image_url", field=models.URLField(blank=True, help_text="Optional external logo URL.", verbose_name="logo URL")),
    ]
