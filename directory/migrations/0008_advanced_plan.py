from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("directory", "0007_communityapplication_plan")]
    operations = [
        migrations.AlterField(
            model_name="communityapplication",
            name="plan",
            field=models.CharField(choices=[("personal", "Personal — €100/year"), ("basic", "Basic — €180/year"), ("advanced", "Advanced — €300/year")], default="personal", max_length=12),
        ),
    ]
