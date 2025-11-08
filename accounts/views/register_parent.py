# accounts/views/register_parent.py
from django.shortcuts import render, redirect
from accounts.forms.registration_parent import ParentRegistrationForm
from accounts.models.profile_parent import ProfileParent
from accounts.services.user_creator import create_user_with_profile
from privacy.models import PrivacyNotice, PrivacyAcceptance

def register_parent_view(request):
    """
    GET: muestra el formulario de Padres
    POST: valida y crea User + ParentProfile
    """
    # Obtener aviso de privacidad activo
    active_privacy = PrivacyNotice.objects.filter(is_active=True).first()
    
    if request.method == "GET":
        return render(request, "accounts/register_parent.html", {
            "form": ParentRegistrationForm(),
            "privacy_notice": active_privacy
        })

    form = ParentRegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, "accounts/register_parent.html", {
            "form": form,
            "privacy_notice": active_privacy
        }, status=400)

    user = create_user_with_profile(
        email=form.cleaned_data["email"],
        password=form.cleaned_data["password"],
        nombres=form.cleaned_data["nombres"],
        apellido_paterno=form.cleaned_data["apellido_paterno"],
        apellido_materno=form.cleaned_data.get("apellido_materno", ""),
        profile_model=ProfileParent
    )
    
    # Registrar aceptación del aviso de privacidad
    if active_privacy:
        PrivacyAcceptance.objects.create(
            user=user,
            privacy_notice=active_privacy
        )
    
    return redirect("accounts:login")  # luego apuntará a tu login propio
