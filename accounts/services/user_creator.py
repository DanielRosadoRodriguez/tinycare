# accounts/services/user_creator.py
from typing import Optional, Type, TypeVar
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from accounts.models.profile_parent import ProfileParent
from accounts.models.profile_specialist import ProfileSpecialist

# TypeVar para permitir ambos perfiles
ProfileT = TypeVar("ProfileT", ProfileParent, ProfileSpecialist)

def create_user_with_profile(
    *,
    email: str,
    password: str,
    nombres: str,
    apellido_paterno: str,
    apellido_materno: str = "",
    profile_model: Type[ProfileT],
    profile_kwargs: Optional[dict] = None,
) -> AbstractBaseUser:
    """
    Crea un usuario (User) y su perfil asociado (Parent o Specialist).
    - profile_model: clase del perfil a crear (ParentProfile o SpecialistProfile)
    - profile_kwargs: campos extra para ese perfil (p.ej., cedula_profesional)
    """
    profile_kwargs = profile_kwargs or {}

    UserModel = get_user_model()
    user = UserModel.objects.create_user(username=email, email=email, password=password)

    # Creamos el perfil sin asignarlo a una variable (evita warning de variable no usada)
    profile_model.objects.create(
        user=user,
        nombres=nombres,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno or "",
        **profile_kwargs,
    )

    return user
