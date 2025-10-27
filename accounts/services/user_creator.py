# accounts/services/user_creator.py
from typing import Type
from django.contrib.auth import get_user_model
from accounts.models import ProfileParent, ProfileSpecialist

User = get_user_model()

def create_user_with_profile(
    *,
    email: str,
    password: str,
    nombres: str,
    apellido_paterno: str,
    apellido_materno: str = "",
    profile_model: Type[ProfileParent | ProfileSpecialist],
    profile_kwargs: dict | None = None
) -> User:
    """
    Crea un usuario (User) y su perfil asociado (Parent o Specialist).
    - profile_model: clase del perfil a crear (ParentProfile o SpecialistProfile)
    - profile_kwargs: campos extra para ese perfil (p.ej., cedula_profesional)
    """
    profile_kwargs = profile_kwargs or {}
    # username=email por simplicidad; luego puedes cambiar a CustomUser si deseas
    user = User.objects.create_user(username=email, email=email, password=password)
    profile = profile_model.objects.create(
        user=user,
        nombres=nombres,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno or "",
        **profile_kwargs
    )
    return user
