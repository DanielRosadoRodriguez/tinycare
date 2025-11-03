from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Importa tu modelo ProfileParent desde su ubicación
from accounts.models.profile_parent import ProfileParent 

class Notification(models.Model):
    """
    Modelo para almacenar notificaciones.
    Usa ContentTypes para apuntar genéricamente a cualquier modelo
    (ej. un Comment o una Vaccine).
    """
    
    # Tipo de notificaciones
    COMMENT = 'comment'
    VACCINE_3_DAYS = 'vaccine_3_days'
    VACCINE_TODAY = 'vaccine_today'
    
    NOTIFICATION_TYPES = [
        (COMMENT, 'Nuevo Comentario'),
        (VACCINE_3_DAYS, 'Recordatorio Vacuna (3 días)'),
        (VACCINE_TODAY, 'Recordatorio Vacuna (Hoy)'),
    ]
    
    # El ProfileParent que recibe la notificación
    user = models.ForeignKey(
        ProfileParent, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        verbose_name="Usuario (Padre/Madre)"
    )
    
    message = models.TextField(verbose_name="Mensaje de la notificación")
    is_read = models.BooleanField(default=False, verbose_name="Leída")
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES,
        verbose_name="Tipo de Notificación"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    # --- Generic Foreign Key (Apunta al objeto que causó la notif) ---
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    
    # El objeto en sí (ej. el Comment o la Vaccine)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-created_at']

    def __str__(self):
        # Asumiendo que ProfileParent tiene un 'user' OneToOne
        return f"Notificación para {self.user.user.email}: {self.message[:30]}..."