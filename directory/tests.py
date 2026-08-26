from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import translation


@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class NavigationPageTests(TestCase):
    def test_each_public_menu_destination_renders(self):
        for name in ("explore", "collaborations", "about", "blog_archive"):
            with self.subTest(name=name):
                response = self.client.get(reverse(name), secure=True)
                self.assertEqual(response.status_code, 200)

    def test_navigation_uses_pages_and_collaborations_label(self):
        with translation.override("en"):
            response = self.client.get(reverse("home"), secure=True)
            self.assertContains(response, reverse("explore"))
            self.assertContains(response, reverse("collaborations"))
            self.assertContains(response, reverse("about"))
            self.assertContains(response, "Collaborations")

    def test_localized_new_pages_render(self):
        for path in ("/es/collaborations/", "/es/about/"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path, secure=True).status_code, 200)
