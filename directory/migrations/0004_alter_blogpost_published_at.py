from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [("directory", "0003_communityapplication")]
    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="published_at",
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="publication date"),
        ),
    ]
