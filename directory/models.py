from django.db import models
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=12, default="✦")
    accent = models.CharField(max_length=20, default="sand")
    def __str__(self): return self.name

class Business(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="businesses")
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    image_url = models.URLField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    review_count = models.PositiveIntegerField(default=0)
    price_label = models.CharField(max_length=40, blank=True)
    featured = models.BooleanField(default=False)
    partner = models.BooleanField(default=True)
    def __str__(self): return self.name


class BlogPost(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    class PostType(models.TextChoices):
        MARKETING = "marketing", "Business marketing"
        SEO = "seo", "Local SEO"
        BUSINESS = "business", "Business spotlight"

    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(max_length=320, help_text="A short introduction shown on the blog archive.")
    content = models.TextField(help_text="Write the article in plain text. Paragraph breaks are preserved.")
    image_url = models.URLField("cover image URL", blank=True)
    author_name = models.CharField(max_length=100, default="Publifuerteventura team")
    post_type = models.CharField(max_length=12, choices=PostType.choices, default=PostType.MARKETING)
    focus_keyword = models.CharField(max_length=160, blank=True, help_text="Main search phrase this article should target.")
    meta_title = models.CharField(max_length=160, blank=True, help_text="SEO page title. Leave blank to use the article title.")
    meta_description = models.CharField(max_length=320, blank=True, help_text="SEO description shown in search results. Leave blank to use the excerpt.")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    featured = models.BooleanField(default=False)
    published_at = models.DateTimeField("publication date", default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-published_at",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})


class CommunityApplication(models.Model):
    class Plan(models.TextChoices):
        BASIC = "basic", "Basic — €100/year"
        ADVANCED = "advanced", "Advanced — €250/year"
        CUSTOM = "custom", "Custom — from €300/year"

    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        APPROVED = "approved", "Approved"
        DECLINED = "declined", "Declined"

    business_name = models.CharField(max_length=140)
    plan = models.CharField(max_length=12, choices=Plan.choices, default=Plan.BASIC)
    contact_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=120)
    category = models.CharField(max_length=100)
    team_size = models.CharField(max_length=40, blank=True)
    message = models.TextField("Tell us about the business")
    accepts_updates = models.BooleanField("Receive community news", default=False)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.business_name


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=80, default="PubliFuerteventura")
    intro = models.TextField(max_length=280, default="Everything happening in Fuerteventura, in one place. Discover our portals, projects and people — then connect directly.")
    hero_title = models.CharField(max_length=120, default="Fuerteventura, all connected.")
    hero_image = models.FileField(upload_to="showcase/", blank=True)
    hero_image_url = models.URLField(blank=True, help_text="Optional alternative to an uploaded image.")
    trailer_url = models.URLField(blank=True, help_text="YouTube, Vimeo or another external trailer link.")
    contact_url = models.URLField(blank=True, default="https://wa.me/")

    class Meta:
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Homepage settings"


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
    image = models.FileField(upload_to="showcase/sponsors/", blank=True)
    image_url = models.URLField(blank=True, help_text="Optional alternative to an uploaded image.")
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "name")

    def __str__(self):
        return self.name


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
