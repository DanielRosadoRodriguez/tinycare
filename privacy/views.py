"""
Vistas para privacy.
"""
from django.shortcuts import render
from privacy.models import PrivacyNotice


def privacy_notice_view(request):
    """
    Muestra el aviso de privacidad activo.
    """
    active_notice = PrivacyNotice.objects.filter(is_active=True).first()
    return render(request, "privacy/privacy_notice.html", {
        "privacy_notice": active_notice
    })
