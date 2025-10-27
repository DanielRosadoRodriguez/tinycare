from django.contrib.auth.models import AbstractBaseUser
from accounts.models.profile_parent import ProfileParent 
from accounts.models.profile_specialist import ProfileSpecialist

def get_user_display_name(user: AbstractBaseUser) -> str:
    """
    Regresa el 'nombre visible' para saludar.
    Busca primero ParentProfile, luego SpecialistProfile. Si no hay, usa el email.
    """
    parent = ProfileParent.objects.filter(user=user).only("nombres", "apellido_paterno").first()
    if parent:
        return f"{parent.nombres} {parent.apellido_paterno}".strip()

    spec = ProfileSpecialist.objects.filter(user=user).only("nombres", "apellido_paterno").first()
    if spec:
        return f"{spec.nombres} {spec.apellido_paterno}".strip()

    return user.email or user.get_username()
