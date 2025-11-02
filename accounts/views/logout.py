from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    """Cierra la sesión del usuario actual."""
    logout(request)
    return redirect('pages:home')