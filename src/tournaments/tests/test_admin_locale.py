from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(ROOT_URLCONF="config.urls")
class AdminLocaleTests(TestCase):
    def test_admin_forces_ukrainian_language(self):
        response = self.client.get(reverse("admin:index"), HTTP_ACCEPT_LANGUAGE="cs,sk;q=0.9")
        self.assertEqual(response.status_code, 302)  # redirect to login

        response = self.client.get(
            reverse("admin:login"),
            HTTP_ACCEPT_LANGUAGE="cs,sk;q=0.9,pl;q=0.8",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Language"), "uk")
        self.assertContains(response, "Увійти")
        self.assertContains(response, "Повернутись на сайт")
        self.assertNotContains(response, "Správa webu")
        self.assertNotContains(response, "Search apps and models")

    def test_admin_empty_state_is_ukrainian(self):
        response = self.client.get(
            reverse("admin:tournaments_player_changelist"),
            HTTP_ACCEPT_LANGUAGE="en;q=0.9",
        )
        self.assertEqual(response.status_code, 302)

        from django.contrib.auth import get_user_model

        admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="testpass123",
        )
        self.client.force_login(admin_user)
        response = self.client.get(
            reverse("admin:tournaments_player_changelist"),
            HTTP_ACCEPT_LANGUAGE="en;q=0.9",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нічого не знайдено")
        self.assertContains(response, "Додати Гравець")
        self.assertNotContains(response, "No results found")
        self.assertNotContains(response, "Select action")
