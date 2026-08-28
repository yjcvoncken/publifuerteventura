from django.db import models
from django.urls import reverse
from django.templatetags.static import static

class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=12, default="✦")
    accent = models.CharField(max_length=20, default="sand")
    def __str__(self): return self.name

class Business(models.Model):
    class HomepageSize(models.IntegerChoices):
        LARGE = 1, "1 — Large"
        SMALL = 2, "2 — Small"

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="businesses")
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    image_url = models.URLField("legacy logo URL", blank=True, help_text="Existing logo fallback. Prefer the dedicated logo fields below.")
    cover_image = models.FileField(upload_to="businesses/covers/", blank=True)
    cover_image_url = models.URLField(blank=True, help_text="Optional external cover image URL.")
    logo = models.FileField(upload_to="businesses/logos/", blank=True)
    logo_url = models.URLField(blank=True, help_text="Optional external logo URL.")
    website_url = models.URLField(blank=True, help_text="Direct website or booking link.")
    price_label = models.CharField(
        max_length=40,
        blank=True,
        help_text="Optional short price note, such as 'From €25' or 'Free'. It is not currently displayed on the website.",
    )
    featured = models.BooleanField(default=False)
    partner = models.BooleanField(default=True)
    homepage_size = models.PositiveSmallIntegerField(
        choices=HomepageSize.choices,
        default=HomepageSize.SMALL,
        help_text="Choose 1 for a large homepage card or 2 for a small card.",
    )
    def __str__(self): return self.name

    @property
    def display_cover_url(self):
        if self.cover_image:
            return self.cover_image.url
        if self.cover_image_url:
            return self.cover_image_url
        generated_covers = {
            "the-remote-escape": "img/business-covers/the-remote-escape.webp",
            "corralejo-info": "img/business-covers/corralejo-info.webp",
            "coworking-punto": "img/business-covers/coworking-punto.webp",
        }
        if self.slug in generated_covers:
            return static(generated_covers[self.slug])
        return self.image_url

    @property
    def display_logo_url(self):
        if self.logo:
            return self.logo.url
        if self.logo_url:
            return self.logo_url
        transparent_logos = {
            "corralejo-info": "img/business-logos/corralejo-info.png",
            "coworking-punto": "img/business-logos/coworking-punto.png",
        }
        if self.slug in transparent_logos:
            return static(transparent_logos[self.slug])
        return self.image_url


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=80, default="PubliFuerteventura")
    intro = models.TextField(max_length=280, default="Everything happening in Fuerteventura, in one place. Discover our portals, projects and people — then connect directly.")
    hero_title = models.CharField(max_length=120, default="Fuerteventura, all connected.")
    hero_image = models.FileField(upload_to="showcase/", blank=True)
    hero_image_data = models.BinaryField(blank=True, null=True, editable=False)
    hero_image_content_type = models.CharField(max_length=100, blank=True, editable=False)
    hero_image_url = models.URLField(blank=True, help_text="Optional alternative to an uploaded image.")
    trailer_url = models.URLField(blank=True, help_text="YouTube, Vimeo or another external trailer link.")
    contact_url = models.URLField(blank=True, default="https://wa.me/")
    team_eyebrow = models.CharField(max_length=60, default="WHO WE ARE")
    team_title = models.CharField(max_length=160, default="People making connections happen.")
    team_intro = models.TextField(max_length=320, default="A local, creative network connecting ideas, projects and people across Fuerteventura.")

    class Meta:
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Homepage settings"

    def save(self, *args, **kwargs):
        # Railway replaces its application filesystem on deploy. Preserve the
        # uploaded hero itself in PostgreSQL so it survives every release.
        uploaded = None
        if self.hero_image and not self.hero_image._committed:
            uploaded = self.hero_image.file
        if uploaded and hasattr(uploaded, "read"):
            try:
                uploaded.seek(0)
                self.hero_image_data = uploaded.read()
                self.hero_image_content_type = getattr(uploaded, "content_type", "") or "image/jpeg"
                uploaded.seek(0)
            except (OSError, ValueError):
                pass
        super().save(*args, **kwargs)

    @property
    def display_hero_url(self):
        if self.hero_image_data and self.pk:
            return reverse("site_hero_image")
        if self.hero_image_url:
            return self.hero_image_url
        if self.hero_image:
            return self.hero_image.url
        return ""


class ShowcaseCard(models.Model):
    title = models.CharField(max_length=100)
    short_text = models.CharField(max_length=180, blank=True)
    image = models.FileField(upload_to="showcase/cards/", blank=True)
    image_url = models.URLField(blank=True, help_text="Optional alternative to an uploaded image.")
    destination_url = models.URLField(blank=True, help_text="Website, WhatsApp, form or portal link. Leave blank to show a non-clickable card.")
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "title")

    def __str__(self):
        return self.title


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True, help_text="Short description shown on the collaborations page.")
    cover_image = models.FileField(upload_to="collaborations/covers/", blank=True)
    cover_image_url = models.URLField(blank=True, help_text="Optional external cover photograph URL.")
    logo = models.FileField(upload_to="collaborations/logos/", blank=True)
    logo_url = models.URLField(blank=True, help_text="Optional external logo URL.")
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "name")
        verbose_name = "Collaboration"
        verbose_name_plural = "Collaborations"

    def __str__(self):
        return self.name

    @property
    def display_cover_url(self):
        if self.cover_image:
            return self.cover_image.url
        return self.cover_image_url

    @property
    def display_logo_url(self):
        if self.logo:
            return self.logo.url
        return self.logo_url


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=160)
    bio = models.TextField(max_length=400, blank=True)
    image = models.FileField(upload_to="showcase/team/", blank=True)
    image_url = models.URLField(blank=True, help_text="Optional alternative to an uploaded image.")
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "name")

    def __str__(self):
        return self.name


class AnalyticsPageView(models.Model):
    path = models.CharField(max_length=300)
    language = models.CharField(max_length=8, blank=True)
    session_hash = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Analytics page view"
        verbose_name_plural = "Analytics"

    def __str__(self):
        return f"{self.path} · {self.created_at:%Y-%m-%d %H:%M}"
