from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("directory", "0006_business_blog_seo")]
    operations = [
        migrations.AddField(
            model_name="communityapplication",
            name="plan",
            field=models.CharField(choices=[("personal", "Personal — €100/year"), ("basic", "Basic — €180/year")], default="personal", max_length=12),
        ),
    ]
