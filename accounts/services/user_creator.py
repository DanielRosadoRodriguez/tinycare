# accounts/services/user_creator.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

def create_user_with_email(email: str, password: str) -> AbstractBaseUser:
    """
    SRP: crear usuario con email y password usando el user model activo.
    """
    UserModel = get_user_model()
    user = UserModel.objects.create_user(username=email, email=email, password=password)
    return user
