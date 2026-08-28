from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("directory", "0025_sponsor_cover_image")]

    operations = [migrations.DeleteModel(name="BlogPost")]
