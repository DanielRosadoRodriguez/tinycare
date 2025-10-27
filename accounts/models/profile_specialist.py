# accounts/models/profile_specialist.py
from django.db import models
from .profile_base import ProfileBase

class ProfileSpecialist(ProfileBase):
    """
    Perfil de Especialista con cédula profesional.
    """
    cedula_profesional = models.CharField(max_length=32)

    class Meta:
        verbose_name = "Especialista"
        verbose_name_plural = "Especialistas"
