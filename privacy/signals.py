from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from privacy.models import Consentimiento

User = get_user_model()


@receiver(post_save, sender=User)
def crear_consentimiento(sender, instance, created, **kwargs):
    """
    Crea automáticamente un registro de Consentimiento cuando se crea un usuario.
    """
    if created:
        Consentimiento.objects.get_or_create(user=instance)
