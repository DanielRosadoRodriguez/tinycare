"""
Modelos para gestión de avisos de privacidad.

- PrivacyNotice: almacena versiones de avisos de privacidad en formato .md
- PrivacyAcceptance: registra qué usuarios aceptaron qué versión del aviso
"""

from django.db import models
from django.contrib.auth import get_user_model
import hashlib

User = get_user_model()


class PrivacyNotice(models.Model):
    """
    Versiones de avisos de privacidad.
    Solo un aviso puede estar activo a la vez.
    """
    content = models.TextField(
        verbose_name="Contenido del aviso",
        help_text="Contenido en formato Markdown"
    )
    content_hash = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
        verbose_name="Hash SHA-256"
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name="Activo"
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Subido por"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    class Meta:
        verbose_name = "Aviso de privacidad"
        verbose_name_plural = "Avisos de privacidad"
        ordering = ["-created_at"]

    def __str__(self):
        status = "Activo" if self.is_active else "Inactivo"
        return f"Aviso {self.id} ({status}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        # Calcular hash SHA-256 del contenido
        if not self.content_hash:
            self.content_hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        
        # Si este aviso se marca como activo, desactivar los demás
        if self.is_active:
            PrivacyNotice.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        
        super().save(*args, **kwargs)


class PrivacyAcceptance(models.Model):
    """
    Registro de aceptación de avisos de privacidad por usuario.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="privacy_acceptances",
        verbose_name="Usuario"
    )
    privacy_notice = models.ForeignKey(
        PrivacyNotice,
        on_delete=models.CASCADE,
        related_name="acceptances",
        verbose_name="Aviso de privacidad"
    )
    accepted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Aceptado el"
    )

    class Meta:
        verbose_name = "Aceptación de aviso de privacidad"
        verbose_name_plural = "Aceptaciones de avisos de privacidad"
        ordering = ["-accepted_at"]
        # Un usuario puede aceptar el mismo aviso solo una vez
        unique_together = [["user", "privacy_notice"]]

    def __str__(self):
        return f"{self.user.email} aceptó aviso {self.privacy_notice.id} el {self.accepted_at.strftime('%Y-%m-%d %H:%M')}"
