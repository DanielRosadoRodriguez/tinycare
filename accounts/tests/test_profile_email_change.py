"""
Test para verificar que el cambio de email en el perfil
sincroniza correctamente el username.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models.profile_parent import ProfileParent

User = get_user_model()


class ProfileEmailChangeTest(TestCase):
    """
    Test para verificar que al cambiar el email en el perfil,
    el username se sincroniza automáticamente y el login funciona
    con el nuevo email.
    """

    def setUp(self):
        """Crear usuario y perfil de prueba."""
        self.client = Client()
        self.old_email = "old@example.com"
        self.new_email = "new@example.com"
        self.password = "TestPass123!"

        # Crear usuario con email original
        self.user = User.objects.create_user(
            username=self.old_email,
            email=self.old_email,
            password=self.password,
        )

        # Crear perfil de padre
        self.profile = ProfileParent.objects.create(
            user=self.user,
            nombres="Juan",
            apellido_paterno="Pérez",
            apellido_materno="García",
        )

    def test_email_change_syncs_username(self):
        """
        Verificar que al cambiar el email, el username se actualiza automáticamente.
        """
        # Login con el email original
        self.client.login(username=self.old_email, password=self.password)

        # Cambiar el email en el perfil
        response = self.client.post(
            reverse("accounts:profile"),
            {
                "username": self.old_email,  # El campo hidden envía el valor viejo
                "email": self.new_email,
                "first_name": "",
                "last_name": "",
                "nombres": "Juan",
                "apellido_paterno": "Pérez",
                "apellido_materno": "García",
            },
        )

        # Verificar que se guardó correctamente
        self.assertEqual(response.status_code, 302)  # Redirect tras éxito

        # Recargar el usuario desde la BD
        self.user.refresh_from_db()

        # Verificar que email y username están sincronizados
        self.assertEqual(self.user.email, self.new_email)
        self.assertEqual(self.user.username, self.new_email)

    def test_login_with_new_email_after_change(self):
        """
        Verificar que después de cambiar el email,
        puedes hacer login con el nuevo email.
        """
        # Cambiar el email directamente
        self.user.email = self.new_email
        self.user.username = self.new_email
        self.user.save()

        # Logout si está logueado
        self.client.logout()

        # Intentar login con el nuevo email
        response = self.client.post(
            reverse("accounts:login"),
            {"email": self.new_email, "password": self.password},
        )

        # Verificar que el login fue exitoso
        self.assertEqual(response.status_code, 302)  # Redirect tras login exitoso
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_cannot_login_with_old_email_after_change(self):
        """
        Verificar que después de cambiar el email,
        NO puedes hacer login con el email antiguo.
        """
        # Cambiar el email
        self.user.email = self.new_email
        self.user.username = self.new_email
        self.user.save()

        # Logout
        self.client.logout()

        # Intentar login con el email ANTIGUO
        response = self.client.post(
            reverse("accounts:login"),
            {"email": self.old_email, "password": self.password},
        )

        # Verificar que el login falló
        self.assertEqual(response.status_code, 400)  # Form inválido
        self.assertFalse(response.wsgi_request.user.is_authenticated)
