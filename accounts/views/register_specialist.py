# accounts/views/register_specialist.py
from django.shortcuts import render, redirect
from accounts.forms.registration_specialist import SpecialistRegistrationForm
from accounts.models.profile_specialist import ProfileSpecialist
from accounts.services.user_creator import create_user_with_profile

def register_specialist_view(request):
    """
    GET: muestra el formulario de Especialistas
    POST: valida y crea User + SpecialistProfile
    """
    if request.method == "GET":
        return render(request, "accounts/register_specialist.html", {"form": SpecialistRegistrationForm()})

    form = SpecialistRegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, "accounts/register_specialist.html", {"form": form}, status=400)

    create_user_with_profile(
        email=form.cleaned_data["email"],
        password=form.cleaned_data["password"],
        nombres=form.cleaned_data["nombres"],
        apellido_paterno=form.cleaned_data["apellido_paterno"],
        apellido_materno=form.cleaned_data.get("apellido_materno", ""),
        profile_model=ProfileSpecialist,
        profile_kwargs={"cedula_profesional": form.cleaned_data["cedula_profesional"]}
    )
    return redirect("/admin/login/")
