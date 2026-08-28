from django.contrib import admin
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, re_path
from django.views.static import serve
from directory import views

urlpatterns = [path("analytics/page-view/", views.analytics_page_view, name="analytics_page_view")]
urlpatterns += [path("site-assets/hero/", views.site_hero_image, name="site_hero_image")]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("pricing/", views.pricing, name="pricing"),
    path("explore/", views.explore, name="explore"),
    path("events/", views.events, name="events"),
    path("collaborations/", views.collaborations, name="collaborations"),
    path("about/", views.about, name="about"),
    path("community/join/", views.join_community, name="join_community"),
    path("community/thanks/", views.join_thanks, name="join_thanks"),
    path("privacy/", views.privacy_policy, name="privacy_policy"),
    path("cookies/", views.cookie_policy, name="cookie_policy"),
    path("terms/", views.terms, name="terms"),
    prefix_default_language=False,
)

urlpatterns += [path("health/", views.health, name="health")]
urlpatterns += [re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT})]
