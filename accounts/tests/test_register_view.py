from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class TestRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_get_ok(self):
        url = reverse("accounts:register")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Crear cuenta", resp.content)

    def test_register_post_creates_user_and_redirects(self):
        url = reverse("accounts:register")
        data = {
            "email": "test@example.com",
            "password": "SuperSegura123",
            "password_confirm": "SuperSegura123",
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp["Location"].endswith("/admin/login/"))
        self.assertTrue(User.objects.filter(email="test@example.com").exists())
