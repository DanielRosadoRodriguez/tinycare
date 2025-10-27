# accounts/models/profile_parent.py
from .profile_base import ProfileBase

class ProfileParent(ProfileBase):
    """
    Perfil de Padre/Madre. No añade campos nuevos, hereda de ProfileBase.
    """
    class Meta:
        verbose_name = "Padre/Madre"
        verbose_name_plural = "Padres/Madres"
