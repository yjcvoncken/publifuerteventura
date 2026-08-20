from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import BlogPost, Business, Category, ShowcaseCard, SiteSettings, Sponsor, TeamMember
from .forms import CommunityApplicationForm


def health(request):
    return JsonResponse({"status": "ok"})

def home(request):
    settings = SiteSettings.objects.first()
    return render(request, "directory/home.html", {
        "site_settings": settings,
        "featured_businesses": Business.objects.select_related("category").filter(featured=True, partner=True)[:8],
        "showcase_cards": ShowcaseCard.objects.filter(active=True)[:3],
        "sponsors": Sponsor.objects.filter(active=True),
        "team_members": TeamMember.objects.filter(active=True),
    })


def pricing(request):
    return render(request, "directory/pricing.html")


def explore(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    businesses = Business.objects.select_related("category").all()
    if query:
        businesses = businesses.filter(Q(name__icontains=query) | Q(tagline__icontains=query) | Q(location__icontains=query))
    if category:
        businesses = businesses.filter(category__slug=category)
    return render(request, "directory/explore.html", {"businesses": businesses, "categories": Category.objects.all(), "query": query, "active_category": category})

def business_detail(request, slug):
    return render(request, "directory/detail.html", {"business": get_object_or_404(Business, slug=slug)})


def blog_archive(request):
    posts = BlogPost.objects.filter(
        status=BlogPost.Status.PUBLISHED,
        published_at__lte=timezone.now(),
    )
    active_type = request.GET.get("type", "")
    visible_posts = posts.filter(post_type=active_type) if active_type in BlogPost.PostType.values else posts
    return render(request, "directory/blog_archive.html", {
        "featured_post": posts.filter(featured=True).first() or posts.first(),
        "posts": visible_posts,
        "active_type": active_type,
        "post_types": BlogPost.PostType.choices,
    })


def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost,
        slug=slug,
        status=BlogPost.Status.PUBLISHED,
        published_at__lte=timezone.now(),
    )
    return render(request, "directory/blog_detail.html", {"post": post})


def join_community(request):
    if request.method == "POST":
        form = CommunityApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("join_thanks")
    else:
        selected_plan = request.GET.get("plan", "basic")
        if selected_plan not in {"basic", "advanced", "custom"}:
            selected_plan = "basic"
        form = CommunityApplicationForm(initial={"plan": selected_plan})
    return render(request, "directory/join.html", {"form": form})


def join_thanks(request):
    return render(request, "directory/join_thanks.html")
