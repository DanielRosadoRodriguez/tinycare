"""
Vistas base para privacy.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from privacy.models import PrivacyNotice, Consentimiento
from privacy.forms import ConsentimientoForm


def privacy_notice_view(request):
    """
    Muestra el aviso de privacidad activo.
    """
    active_notice = PrivacyNotice.objects.filter(is_active=True).first()
    return render(request, "privacy/privacy_notice.html", {
        "privacy_notice": active_notice
    })


@login_required
def actualizar_consentimientos_view(request):
    """
    Actualiza los consentimientos de privacidad del usuario.
    """
    if request.method == "POST":
        consentimiento, created = Consentimiento.objects.get_or_create(user=request.user)
        form = ConsentimientoForm(request.POST, instance=consentimiento)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Preferencias de privacidad actualizadas correctamente.")
        else:
            messages.error(request, "Error al actualizar las preferencias de privacidad.")
    
    return redirect("accounts:profile")
