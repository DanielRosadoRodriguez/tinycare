"""
Tests para la app babies.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date

from babies.models import Baby
from accounts.models.profile_parent import ProfileParent

User = get_user_model()


class BabyModelTest(TestCase):
    """Tests para el modelo Baby."""

    def setUp(self):
        # Crear usuario y perfil de padre
        self.user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        self.parent = ProfileParent.objects.create(
            user=self.user,
            nombres="Juan",
            apellido_paterno="Pérez",
            apellido_materno="García",
        )

    def test_create_baby(self):
        """Verificar que se puede crear un bebé."""
        baby = Baby.objects.create(
            parent=self.parent,
            nombre="María",
            fecha_nacimiento=date(2024, 1, 15),
            sexo="F",
            peso=3.5,
        )
        self.assertEqual(baby.nombre, "María")
        self.assertEqual(baby.sexo, "F")
        self.assertEqual(baby.parent, self.parent)

    def test_edad_en_meses(self):
        """Verificar cálculo de edad en meses."""
        baby = Baby.objects.create(
            parent=self.parent,
            nombre="Pedro",
            fecha_nacimiento=date(2024, 1, 1),
            sexo="M",
        )
        edad = baby.edad_en_meses()
        self.assertIsInstance(edad, int)
        self.assertGreaterEqual(edad, 0)

    def test_baby_str(self):
        """Verificar representación en string del bebé."""
        baby = Baby.objects.create(
            parent=self.parent,
            nombre="Ana",
            fecha_nacimiento=date(2024, 6, 1),
            sexo="F",
        )
        self.assertEqual(str(baby), "Ana (Femenino)")


class BabyViewsTest(TestCase):
    """Tests para las vistas de babies."""

    def setUp(self):
        self.client = Client()
        # Crear usuario y perfil de padre
        self.user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        self.parent = ProfileParent.objects.create(
            user=self.user,
            nombres="Juan",
            apellido_paterno="Pérez",
        )
        # Crear un bebé de prueba
        self.baby = Baby.objects.create(
            parent=self.parent,
            nombre="María",
            fecha_nacimiento=date(2024, 1, 15),
            sexo="F",
        )

    def test_baby_list_requires_login(self):
        """Verificar que la lista de bebés requiere login."""
        response = self.client.get(reverse("babies:baby_list"))
        self.assertEqual(response.status_code, 302)  # Redirección a login

    def test_baby_list_authenticated(self):
        """Verificar que un usuario autenticado puede ver su lista de bebés."""
        self.client.login(username="test@example.com", password="testpass123")
        response = self.client.get(reverse("babies:baby_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "María")

    def test_baby_detail_owner_can_access(self):
        """Verificar que el padre propietario puede ver el detalle."""
        self.client.login(username="test@example.com", password="testpass123")
        response = self.client.get(
            reverse("babies:baby_detail", kwargs={"pk": self.baby.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "María")

    def test_create_baby_view(self):
        """Verificar creación de bebé via formulario."""
        self.client.login(username="test@example.com", password="testpass123")
        response = self.client.post(
            reverse("babies:baby_create"),
            {
                "nombre": "Pedro",
                "fecha_nacimiento": "2024-06-01",
                "sexo": "M",
                "peso": "3.2",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirección tras éxito
        self.assertTrue(Baby.objects.filter(nombre="Pedro").exists())

