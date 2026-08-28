from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("directory", "0026_remove_blogpost")]

    operations = [
        # Renames preserve every existing collaboration image and URL; they
        # simply become the dedicated logo fields in the admin.
        migrations.RenameField(model_name="sponsor", old_name="image", new_name="logo"),
        migrations.RenameField(model_name="sponsor", old_name="image_url", new_name="logo_url"),
        migrations.AlterField(
            model_name="sponsor",
            name="logo",
            field=models.FileField(blank=True, upload_to="collaborations/logos/"),
        ),
        migrations.AlterField(
            model_name="sponsor",
            name="logo_url",
            field=models.URLField(blank=True, help_text="Optional external logo URL."),
        ),
    ]
