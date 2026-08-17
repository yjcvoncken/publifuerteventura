from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import BlogPost, Business, Category, CommunityApplication


admin.site.site_header = "Publifuerteventura administration"
admin.site.site_title = "Publifuerteventura admin"
admin.site.index_title = "Directory management"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "accent", "business_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)

    @admin.display(description="Businesses")
    def business_count(self, category):
        return category.businesses.count()


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = (
        "name", "category", "location", "rating", "featured", "partner"
    )
    list_filter = ("partner", "featured", "category", "location")
    search_fields = ("name", "tagline", "description", "location")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("featured", "partner")
    list_select_related = ("category",)
    ordering = ("name",)
    fieldsets = (
        ("Business", {"fields": ("name", "slug", "category", "tagline", "description")}),
        ("Location and presentation", {"fields": ("location", "image_url", "price_label")}),
        ("Trust signals", {"fields": ("rating", "review_count", "partner", "featured")}),
    )


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "post_type", "status", "featured", "published_at", "updated_at", "view_post")
    list_filter = ("post_type", "status", "featured", "published_at")
    search_fields = ("title", "excerpt", "content", "author_name")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("status", "featured")
    actions = ("publish_now", "move_to_drafts")
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    fieldsets = (
        ("Write", {"fields": ("title", "slug", "excerpt", "content", "image_url"), "description": "Write useful content for Fuerteventura business owners and explain how online visibility can bring them customers."}),
        ("Search visibility", {"fields": ("focus_keyword", "meta_title", "meta_description"), "description": "Target one clear phrase that a local business owner might search. Keep the SEO title and description natural and specific."}),
        ("Publish", {"fields": ("post_type", "author_name", "status", "featured", "published_at"), "description": "Choose Published to make the post visible. A future publication date schedules it automatically."}),
    )

    @admin.display(description="Public page")
    def view_post(self, post):
        if post.status == post.Status.PUBLISHED and post.published_at <= timezone.now():
            return format_html('<a href="{}" target="_blank">View ↗</a>', post.get_absolute_url())
        return "—"

    @admin.action(description="Publish selected posts now")
    def publish_now(self, request, queryset):
        count = queryset.update(status=BlogPost.Status.PUBLISHED, published_at=timezone.now())
        self.message_user(request, f"{count} post(s) published.")

    @admin.action(description="Move selected posts back to drafts")
    def move_to_drafts(self, request, queryset):
        count = queryset.update(status=BlogPost.Status.DRAFT)
        self.message_user(request, f"{count} post(s) moved to drafts.")


@admin.register(CommunityApplication)
class CommunityApplicationAdmin(admin.ModelAdmin):
    list_display = ("business_name", "plan", "contact_name", "location", "category", "status", "created_at")
    list_filter = ("plan", "status", "category", "location", "accepts_updates", "created_at")
    search_fields = ("business_name", "contact_name", "email", "phone", "message")
    list_editable = ("status",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    fieldsets = (
        ("Application", {"fields": ("plan", "business_name", "contact_name", "email", "phone", "website")}),
        ("Business", {"fields": ("location", "category", "team_size", "message", "accepts_updates")}),
        ("Review", {"fields": ("status", "admin_notes", "created_at", "updated_at")}),
    )
