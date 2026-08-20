from django.db import migrations


def move_to_businesses(apps, schema_editor):
    Category = apps.get_model("directory", "Category")
    Business = apps.get_model("directory", "Business")
    ShowcaseCard = apps.get_model("directory", "ShowcaseCard")

    entries = (
        {
            "category": ("Work & Travel", "work-travel", "coral"),
            "name": "The Remote Escape", "slug": "the-remote-escape",
            "tagline": "Find paid short-term work for your next stay in Spain.",
            "description": "A platform connecting travelers with clear, paid short-term work opportunities.",
            "location": "Fuerteventura & Spain", "website_url": "https://theremoteescape.com/",
            "image_url": "https://theremoteescape.com/static/theremoteescape-mark.43f83534365d.svg",
        },
        {
            "category": ("Local Guides", "local-guides", "blue"),
            "name": "Corralejo.info", "slug": "corralejo-info",
            "tagline": "The complete local guide to Corralejo and Fuerteventura.",
            "description": "Activities, practical information, local services and everything you need to discover Fuerteventura.",
            "location": "Corralejo", "website_url": "https://www.corralejo.info/",
            "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=85",
        },
        {
            "category": ("Coworking", "coworking", "sage"),
            "name": "Coworking Punto", "slug": "coworking-punto",
            "tagline": "A shared space for work, ideas and local connections.",
            "description": "A professional coworking and meeting point for Fuerteventura's local and remote-working community.",
            "location": "Corralejo", "website_url": "https://coworkingpunto.com/",
            "image_url": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1200&q=85",
        },
    )
    for entry in entries:
        category_name, category_slug, accent = entry.pop("category")
        category, _ = Category.objects.get_or_create(slug=category_slug, defaults={"name": category_name, "accent": accent})
        slug = entry.pop("slug")
        Business.objects.update_or_create(slug=slug, defaults={**entry, "category": category, "featured": True, "partner": True})
    ShowcaseCard.objects.filter(title__in=["The Remote Escape", "Corralejo.info", "Coworking Punto"]).delete()


class Migration(migrations.Migration):
    dependencies = [("directory", "0015_business_website_url")]
    operations = [migrations.RunPython(move_to_businesses, migrations.RunPython.noop)]
