"""
Modelo Baby - Registro de información de bebés.

Un bebé pertenece a un único ProfileParent (1:N).
Incluye campos obligatorios (nombre, fecha_nacimiento, sexo) y opcionales
(peso, alergias, condiciones_salud) según requisitos del proyecto.

Los campos sensibles (alergias, condiciones_salud) se cifran con AES-256-GCM.
"""

from django.db import models
from accounts.models.profile_parent import ProfileParent
from core.fields import EncryptedTextField


class Baby(models.Model):
    """
    Modelo para registrar información de bebés.
    Relación: 1 padre puede tener N hijos, pero 1 hijo pertenece a 1 padre.
    """

    SEXO_CHOICES = [
        ("M", "Masculino"),
        ("F", "Femenino"),
        ("O", "Otro"),
    ]

    # Relación con el padre/madre (ProfileParent)
    parent = models.ForeignKey(
        ProfileParent,
        on_delete=models.CASCADE,
        related_name="babies",
        verbose_name="Padre/Madre",
    )

    # Campos obligatorios
    nombre = models.CharField(max_length=100, verbose_name="Nombre del bebé")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name="Sexo")

    # Campos opcionales
    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Peso (kg)",
        help_text="Peso del bebé en kilogramos",
    )
    
    # Campos sensibles - cifrados con AES-256-GCM
    alergias = EncryptedTextField(
        blank=True,
        verbose_name="Alergias",
        help_text="Registra alergias conocidas del bebé (cifrado)",
    )
    condiciones_salud = EncryptedTextField(
        blank=True,
        verbose_name="Condiciones de salud",
        help_text="Condiciones médicas, enfermedades crónicas, etc. (cifrado)",
    )

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Bebé"
        verbose_name_plural = "Bebés"
        ordering = ["-fecha_nacimiento"]  # Más recientes primero

    def __str__(self):
        return f"{self.nombre} ({self.get_sexo_display()})"

    def edad_en_meses(self):
        """Calcula la edad del bebé en meses."""
        from datetime import date

        hoy = date.today()
        meses = (hoy.year - self.fecha_nacimiento.year) * 12
        meses += hoy.month - self.fecha_nacimiento.month
        if hoy.day < self.fecha_nacimiento.day:
            meses -= 1
        return max(0, meses)
