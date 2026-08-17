from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from directory import views

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("pricing/", views.pricing, name="pricing"),
    path("explore/", views.explore, name="explore"),
    path("business/<slug:slug>/", views.business_detail, name="business_detail"),
    path("blog/", views.blog_archive, name="blog_archive"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("community/join/", views.join_community, name="join_community"),
    path("community/thanks/", views.join_thanks, name="join_thanks"),
    prefix_default_language=False,
)

urlpatterns += [path("health/", views.health, name="health")]
