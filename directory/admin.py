from datetime import timedelta

from django.contrib import admin
from django.db.models import Count
from django.utils import timezone


from .models import (
    AnalyticsPageView, Business, Category,
    SiteSettings, Sponsor, TeamMember,
)


admin.site.site_header = "Publifuerteventura administration"
admin.site.site_title = "Publifuerteventura admin"
admin.site.index_title = "Showcase management"


class OrderedContentAdmin(admin.ModelAdmin):
    list_display = ("title_or_name", "order", "active")
    list_editable = ("order", "active")
    list_filter = ("active",)
    ordering = ("order",)

    @admin.display(description="Content")
    def title_or_name(self, obj):
        return str(obj)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identity", {"fields": ("site_name",)}),
        ("Homepage introduction", {"fields": ("hero_title", "intro", "hero_image", "hero_image_url", "trailer_url")}),
        ("Who we are", {"fields": ("team_eyebrow", "team_title", "team_intro"), "description": "Edit the section heading here. Manage the people listed in this section under Team members."}),
        ("Contact", {"fields": ("contact_url",)}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Sponsor)
class SponsorAdmin(OrderedContentAdmin):
    search_fields = ("name", "link")
    fieldsets = (
        ("Collaboration", {"fields": ("name", "description", "link")}),
        ("Cover image", {"fields": ("cover_image", "cover_image_url"), "description": "Large photograph displayed across the card, just like a business cover."}),
        ("Logo", {"fields": ("logo", "logo_url"), "description": "Small transparent logo displayed over the cover, just like a business logo."}),
        ("Visibility and position", {"fields": ("order", "active")}),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(OrderedContentAdmin):
    search_fields = ("name", "role", "bio")
    fieldsets = (
        ("Person or collaborator", {"fields": ("name", "role", "bio", "image", "image_url", "link")}),
        ("Visibility and position", {"fields": ("order", "active")}),
    )


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
        "name", "category", "location", "homepage_size", "featured", "partner"
    )

    list_filter = ("partner", "featured", "category", "location")
    search_fields = ("name", "tagline", "description", "location")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("homepage_size", "featured", "partner")
    list_select_related = ("category",)
    ordering = ("name",)
    fieldsets = (
        ("Business", {"fields": ("name", "slug", "category", "tagline", "description")}),
        ("Cover image", {"fields": ("cover_image", "cover_image_url"), "description": "Large full-card photograph. Upload an image or provide an external URL."}),
        ("Logo", {"fields": ("logo", "logo_url", "image_url"), "description": "Small business logo displayed over the cover. The legacy URL keeps existing logos working."}),
        ("Location and link", {"fields": ("location", "website_url", "price_label")}),
        ("Homepage display", {"fields": ("featured", "homepage_size", "partner"), "description": "Choose whether this featured business uses a large (1) or small (2) card on the homepage."}),
    )


@admin.register(AnalyticsPageView)
class AnalyticsPageViewAdmin(admin.ModelAdmin):
    change_list_template = "admin/directory/analyticspageview/change_list.html"
    list_display = ("path", "language", "created_at")
    list_filter = ("language", "created_at")
    search_fields = ("path",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        last_30_days = timezone.now() - timedelta(days=30)
        recent = AnalyticsPageView.objects.filter(created_at__gte=last_30_days)
        dashboard = {
            "total_views": AnalyticsPageView.objects.count(),
            "recent_views": recent.count(),
            "recent_sessions": recent.exclude(session_hash="").values("session_hash").distinct().count(),
            "top_pages": list(recent.values("path").annotate(views=Count("id")).order_by("-views")[:8]),
        }
        return super().changelist_view(request, {**(extra_context or {}), **dashboard})

