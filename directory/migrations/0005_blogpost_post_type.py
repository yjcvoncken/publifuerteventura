from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("directory", "0004_alter_blogpost_published_at")]
    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="post_type",
            field=models.CharField(choices=[("business", "New business"), ("news", "About Publifuerteventura"), ("guide", "Island guide")], default="news", max_length=12),
        ),
    ]
