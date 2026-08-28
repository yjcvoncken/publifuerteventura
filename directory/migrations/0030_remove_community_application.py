from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("directory", "0029_remove_business_ratings")]

    operations = [migrations.DeleteModel(name="CommunityApplication")]
