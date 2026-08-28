from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import translation

from .models import AnalyticsPageView, Business, SiteSettings


@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class NavigationPageTests(TestCase):
    def test_each_public_menu_destination_renders(self):
        for name in ("explore", "events", "collaborations", "about", "blog_archive"):
            with self.subTest(name=name):
                response = self.client.get(reverse(name), secure=True)
                self.assertEqual(response.status_code, 200)

    def test_navigation_uses_pages_and_collaborations_label(self):
        with translation.override("en"):
            response = self.client.get(reverse("home"), secure=True)
            self.assertContains(response, reverse("explore"))
            self.assertContains(response, reverse("events"))
            self.assertContains(response, reverse("collaborations"))
            self.assertContains(response, reverse("about"))
            self.assertContains(response, "Collaborations")
            self.assertContains(response, "https://wa.me/34608908555")

    def test_localized_new_pages_render(self):
        for path in ("/es/events/", "/es/collaborations/", "/es/about/"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path, secure=True).status_code, 200)

    @override_settings(GOOGLE_CALENDAR_ID="events@example.com", GOOGLE_CALENDAR_TIME_ZONE="Atlantic/Canary")
    def test_events_page_embeds_configured_google_calendar(self):
        response = self.client.get(reverse("events"), secure=True)
        self.assertContains(response, "calendar.google.com/calendar/embed?")
        self.assertContains(response, "events%40example.com")
        self.assertContains(response, "Atlantic%2FCanary")
        self.assertContains(response, "mode=AGENDA")
        self.assertContains(response, "showTabs=0")

    def test_current_business_uses_generated_cover_and_separate_logo(self):
        business = Business.objects.get(slug="the-remote-escape")
        self.assertIn("business-covers/the-remote-escape", business.display_cover_url)
        self.assertEqual(business.display_logo_url, business.image_url)
        corralejo = Business.objects.get(slug="corralejo-info")
        self.assertIn("business-logos/corralejo-info", corralejo.display_logo_url)

    def test_analytics_requires_consent_and_hashes_session(self):
        endpoint = reverse("analytics_page_view")
        payload = {"path": "/about/", "language": "en", "session": "anonymous-test"}
        self.client.cookies["publifuerte_cookie_choice"] = "essential"
        self.client.post(endpoint, payload, content_type="application/json", secure=True)
        self.assertEqual(AnalyticsPageView.objects.count(), 0)
        self.client.cookies["publifuerte_cookie_choice"] = "accepted"
        response = self.client.post(endpoint, payload, content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 201)
        page_view = AnalyticsPageView.objects.get()
        self.assertEqual(page_view.path, "/about/")
        self.assertNotEqual(page_view.session_hash, "anonymous-test")

    def test_analytics_dashboard_renders_in_admin(self):
        admin_user = get_user_model().objects.create_superuser("analytics-admin", "admin@example.com", "test-password")
        self.client.force_login(admin_user)
        response = self.client.get(reverse("admin:directory_analyticspageview_changelist"), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "All-time views")

    def test_uploaded_hero_is_stored_and_served_from_database(self):
        image_bytes = b"database-backed-image"
        site_settings = SiteSettings.objects.first() or SiteSettings()
        site_settings.hero_image = SimpleUploadedFile(
            "hero.webp", image_bytes, content_type="image/webp"
        )
        site_settings.save()
        site_settings.refresh_from_db()
        self.assertEqual(bytes(site_settings.hero_image_data), image_bytes)
        self.assertEqual(site_settings.display_hero_url, reverse("site_hero_image"))

        response = self.client.get(reverse("site_hero_image"), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, image_bytes)
        self.assertEqual(response["Content-Type"], "image/webp")
