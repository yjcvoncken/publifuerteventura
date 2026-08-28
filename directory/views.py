from django.db.models import Q
import hashlib
import json
from urllib.parse import urlencode

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import AnalyticsPageView, Business, Category, SiteSettings, Sponsor, TeamMember
from .forms import CommunityApplicationForm


def health(request):
    return JsonResponse({"status": "ok"})


def site_hero_image(request):
    site_settings = SiteSettings.objects.only(
        "hero_image_data", "hero_image_content_type"
    ).first()
    if not site_settings or not site_settings.hero_image_data:
        return HttpResponse(status=404)
    response = HttpResponse(
        bytes(site_settings.hero_image_data),
        content_type=site_settings.hero_image_content_type or "image/jpeg",
    )
    response["Cache-Control"] = "public, max-age=3600"
    response["X-Content-Type-Options"] = "nosniff"
    return response


@csrf_exempt
@require_POST
def analytics_page_view(request):
    if request.COOKIES.get("publifuerte_cookie_choice") != "accepted":
        return JsonResponse({}, status=204)
    try:
        payload = json.loads(request.body or b"{}")
    except (TypeError, ValueError):
        return JsonResponse({"error": "invalid payload"}, status=400)
    path = str(payload.get("path", ""))[:300]
    if not path.startswith("/") or path.startswith(("/admin/", "/static/", "/media/")):
        return JsonResponse({}, status=204)
    anonymous_id = str(payload.get("session", ""))[:100]
    session_hash = hashlib.sha256(
        f"{settings.SECRET_KEY}:{anonymous_id}".encode()
    ).hexdigest() if anonymous_id else ""
    AnalyticsPageView.objects.create(
        path=path,
        language=str(payload.get("language", ""))[:8],
        session_hash=session_hash,
    )
    return JsonResponse({"recorded": True}, status=201)

def privacy_policy(request): return render(request, "directory/privacy_policy.html")
def cookie_policy(request): return render(request, "directory/cookie_policy.html")
def terms(request): return render(request, "directory/terms.html")

def home(request):
    settings = SiteSettings.objects.first()
    return render(request, "directory/home.html", {
        "site_settings": settings,
        "featured_businesses": Business.objects.select_related("category").filter(featured=True, partner=True)[:8],
        "collaborations": Sponsor.objects.filter(active=True),
        "team_members": TeamMember.objects.filter(active=True),
    })


def pricing(request):
    return render(request, "directory/pricing.html")


def events(request):
    calendar_id = settings.GOOGLE_CALENDAR_ID
    calendar_embed_url = ""
    if calendar_id:
        calendar_embed_url = "https://calendar.google.com/calendar/embed?" + urlencode({
            "src": calendar_id,
            "ctz": settings.GOOGLE_CALENDAR_TIME_ZONE,
            "showTitle": 0,
            "showPrint": 0,
            "showCalendars": 0,
            "showTz": 0,
            "showTabs": 0,
            "mode": "AGENDA",
        })
    return render(request, "directory/events.html", {
        "calendar_embed_url": calendar_embed_url,
    })


def collaborations(request):
    return render(request, "directory/collaborations.html", {
        "collaborations": Sponsor.objects.filter(active=True),
    })


def about(request):
    return render(request, "directory/about.html", {
        "site_settings": SiteSettings.objects.first(),
        "team_members": TeamMember.objects.filter(active=True),
    })


def explore(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    businesses = Business.objects.select_related("category").all()
    if query:
        businesses = businesses.filter(Q(name__icontains=query) | Q(tagline__icontains=query) | Q(location__icontains=query))
    if category:
        businesses = businesses.filter(category__slug=category)
    categories = Category.objects.all()
    rows = []
    for item in categories:
        row_businesses = list(businesses.filter(category=item))
        if row_businesses:
            rows.append({"category": item, "businesses": row_businesses})
    return render(request, "directory/explore.html", {
        "businesses": businesses,
        "business_rows": rows,
        "categories": categories,
        "query": query,
        "active_category": category,
    })

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
