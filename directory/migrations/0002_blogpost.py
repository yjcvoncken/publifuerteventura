from django.db import migrations, models
from django.utils import timezone


def seed_blog(apps, schema_editor):
    BlogPost = apps.get_model("directory", "BlogPost")
    BlogPost.objects.create(
        title="A slow day in El Cotillo",
        slug="slow-day-el-cotillo",
        excerpt="Where to swim, eat and watch the sun disappear on Fuerteventura's north-west coast.",
        content="Start with the lagoon beaches north of the village, where the water is usually calm and startlingly clear. Arrive early, bring water and leave the shoreline exactly as you found it.\n\nFor lunch, wander back toward the old harbour. The best tables are the simple ones: fresh fish, papas arrugadas and a view of the water. Leave room for a coffee while the village settles into its afternoon rhythm.\n\nBefore sunset, follow the coast south toward the cliffs. The light turns the landscape copper and, on a clear evening, Lanzarote seems close enough to touch.",
        image_url="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=85",
        author_name="Publifuerteventura team",
        status="published",
        featured=True,
        published_at=timezone.now(),
    )
    BlogPost.objects.create(
        title="The island guide to hiring local",
        slug="island-guide-hiring-local",
        excerpt="A few useful questions to ask before booking a trade, class or service on the island.",
        content="Good local businesses are often busy, personal and built on word of mouth. A clear first message helps: say where you are, what you need and when you need it.\n\nAsk what is included in the price and whether materials, travel or equipment cost extra. For larger jobs, get the details in writing.\n\nMost importantly, choose people who communicate clearly. Every business on Publifuerteventura is a reviewed partner, giving you a confident place to start.",
        image_url="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1600&q=85",
        author_name="Publifuerteventura team",
        status="published",
        published_at=timezone.now(),
    )


class Migration(migrations.Migration):
    dependencies = [("directory", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("slug", models.SlugField(unique=True)),
                ("excerpt", models.TextField(help_text="A short introduction shown on the blog archive.", max_length=320)),
                ("content", models.TextField(help_text="Write the article in plain text. Paragraph breaks are preserved.")),
                ("image_url", models.URLField(blank=True, verbose_name="cover image URL")),
                ("author_name", models.CharField(default="Publifuerteventura team", max_length=100)),
                ("status", models.CharField(choices=[("draft", "Draft"), ("published", "Published")], default="draft", max_length=12)),
                ("featured", models.BooleanField(default=False)),
                ("published_at", models.DateTimeField(verbose_name="publication date")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ("-published_at",)},
        ),
        migrations.RunPython(seed_blog, migrations.RunPython.noop),
    ]
