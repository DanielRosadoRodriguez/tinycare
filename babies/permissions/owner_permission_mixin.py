"""
Mixin de permisos para asegurar que solo los padres propietarios
puedan ver/editar/eliminar sus propios bebés.
"""

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from babies.models import Baby
from accounts.models.profile_parent import ProfileParent


class BabyOwnerPermissionMixin:
    """
    Mixin que verifica que el usuario autenticado sea el padre/madre
    propietario del bebé antes de permitir acceso a la vista.
    """

    def dispatch(self, request, *args, **kwargs):
        # Obtener el bebé
        baby = get_object_or_404(Baby, pk=kwargs.get("pk"))

        # Verificar que el usuario tenga un ProfileParent
        try:
            parent_profile = ProfileParent.objects.get(user=request.user)
        except ProfileParent.DoesNotExist:
            raise PermissionDenied(
                "Solo los padres/madres pueden acceder a esta sección."
            )

        # Verificar que el bebé pertenezca al padre autenticado
        if baby.parent != parent_profile:
            raise PermissionDenied("No tienes permiso para acceder a este bebé.")

        return super().dispatch(request, *args, **kwargs)
