from django.db import migrations, models
import django.db.models.deletion

def seed(apps, schema_editor):
    Category = apps.get_model("directory", "Category")
    Business = apps.get_model("directory", "Business")
    cats = {}
    data = [
        ("Eat & drink", "eat-drink", "🍴", "coral"), ("Ocean & adventure", "ocean-adventure", "⌁", "blue"),
        ("Home & trades", "home-trades", "⌂", "ochre"), ("Wellness", "wellness", "✦", "sage"),
        ("Transport", "transport", "↗", "violet"), ("Creative & events", "creative-events", "✺", "pink"),
    ]
    for name, slug, icon, accent in data:
        cats[slug] = Category.objects.create(name=name, slug=slug, icon=icon, accent=accent)
    items = [
        ("Casa Manolo", "casa-manolo", "eat-drink", "Wood-fired Canarian cooking by the sea", "El Cotillo", "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1200&q=85", "4.9", 128, "€€", True),
        ("North Shore Surf Co.", "north-shore-surf", "ocean-adventure", "Small-group surf lessons for every level", "Corralejo", "https://images.unsplash.com/photo-1502680390469-be75c86b636f?auto=format&fit=crop&w=1200&q=85", "4.8", 94, "From €45", True),
        ("Luna Studio", "luna-studio", "wellness", "Yoga, movement and slow island mornings", "Lajares", "https://images.unsplash.com/photo-1545389336-cf090694435e?auto=format&fit=crop&w=1200&q=85", "4.9", 76, "From €14", True),
        ("Majorero Homes", "majorero-homes", "home-trades", "Trusted property care, repairs and renovations", "Island-wide", "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1200&q=85", "4.7", 51, "Quote", True),
        ("Volcano Wheels", "volcano-wheels", "transport", "Freedom to explore, without the airport queues", "Puerto del Rosario", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=1200&q=85", "4.8", 203, "From €28/day", True),
        ("Isla Picnic", "isla-picnic", "creative-events", "Beautifully styled picnics for your people", "Fuerteventura", "https://images.unsplash.com/photo-1528605248644-14dd04022da1?auto=format&fit=crop&w=1200&q=85", "5.0", 39, "From €120", True),
    ]
    for n,s,c,t,l,img,r,rc,p,f in items:
        Business.objects.create(category=cats[c], name=n, slug=s, tagline=t, description=t+". A trusted local team, hand-picked for great service and a genuine love of Fuerteventura.", location=l, image_url=img, rating=r, review_count=rc, price_label=p, featured=f)

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Category", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=80)), ("slug", models.SlugField(unique=True)), ("icon", models.CharField(default="✦", max_length=12)), ("accent", models.CharField(default="sand", max_length=20))]),
        migrations.CreateModel(name="Business", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=120)), ("slug", models.SlugField(unique=True)), ("tagline", models.CharField(max_length=180)), ("description", models.TextField(blank=True)), ("location", models.CharField(max_length=100)), ("image_url", models.URLField()), ("rating", models.DecimalField(decimal_places=1, default=5, max_digits=2)), ("review_count", models.PositiveIntegerField(default=0)), ("price_label", models.CharField(blank=True, max_length=40)), ("featured", models.BooleanField(default=False)), ("partner", models.BooleanField(default=True)), ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="businesses", to="directory.category"))]),
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
