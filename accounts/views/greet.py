from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.services.user_display_name import get_user_display_name

@login_required
def greet_view(request):
    """
    Muestra 'Hola, <nombre>' usando el servicio de nombre visible.
    """
    display_name = get_user_display_name(request.user)
    return render(request, "accounts/greet.html", {"display_name": display_name})
