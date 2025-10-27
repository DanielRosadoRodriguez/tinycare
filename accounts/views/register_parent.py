# accounts/views/register_parent.py
from django.shortcuts import render, redirect
from accounts.forms.registration_parent import ParentRegistrationForm
from accounts.models.profile_parent import ProfileParent
from accounts.services.user_creator import create_user_with_profile

def register_parent_view(request):
    """
    GET: muestra el formulario de Padres
    POST: valida y crea User + ParentProfile
    """
    if request.method == "GET":
        return render(request, "accounts/register_parent.html", {"form": ParentRegistrationForm()})

    form = ParentRegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, "accounts/register_parent.html", {"form": form}, status=400)

    create_user_with_profile(
        email=form.cleaned_data["email"],
        password=form.cleaned_data["password"],
        nombres=form.cleaned_data["nombres"],
        apellido_paterno=form.cleaned_data["apellido_paterno"],
        apellido_materno=form.cleaned_data.get("apellido_materno", ""),
        profile_model=ProfileParent
    )
    return redirect("/admin/login/")  # luego apuntará a tu login propio
