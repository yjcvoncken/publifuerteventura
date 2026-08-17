from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("directory", "0002_blogpost")]
    operations = [
        migrations.CreateModel(
            name="CommunityApplication",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("business_name", models.CharField(max_length=140)),
                ("contact_name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(blank=True, max_length=40)),
                ("website", models.URLField(blank=True)),
                ("location", models.CharField(max_length=120)),
                ("category", models.CharField(max_length=100)),
                ("team_size", models.CharField(blank=True, max_length=40)),
                ("message", models.TextField(verbose_name="Tell us about the business")),
                ("accepts_updates", models.BooleanField(default=False, verbose_name="Receive community news")),
                ("status", models.CharField(choices=[("new", "New"), ("contacted", "Contacted"), ("approved", "Approved"), ("declined", "Declined")], default="new", max_length=12)),
                ("admin_notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ("-created_at",)},
        ),
    ]
