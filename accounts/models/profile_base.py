# accounts/models/profile_base.py
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

User = get_user_model()

class ProfileBase(models.Model):
    """
    ABSTRACT: Campos comunes para cualquier perfil.
    """

    user = models.OneToOneField(User, 
                                on_delete=models.CASCADE, 
                                primary_key=True, 
                                related_name="%(app_label)s_%(class)s_user"
                                )

    nombres = models.CharField(max_length=80)
    apellido_paterno = models.CharField(max_length=80)
    apellido_materno = models.CharField(max_length=80, blank=True)

    class Meta:
        abstract = True
        constraints = [
            UniqueConstraint(Lower("email"),
                             name="%(app_label)s_%(class)s_email_ci_uniq"),
        ]

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno} ({self.user.email})"
