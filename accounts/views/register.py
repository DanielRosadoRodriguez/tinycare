# accounts/views/register.py
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from accounts.forms.registration import RegistrationForm
from accounts.services.user_creator import create_user_with_email

def register_view(request: HttpRequest) -> HttpResponse:
    """
    SRP: Vista para registrar un usuario.
    GET: muestra formulario
    POST: valida y crea usuario, redirige a login (lo implementaremos después)
    """
    if request.method == "GET":
        return render(request, "accounts/register.html", {"form": RegistrationForm()})

    form = RegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, "accounts/register.html", {"form": form}, status=400)

    create_user_with_email(
        email=form.cleaned_data["email"],
        password=form.cleaned_data["password"]
    )
    # Por ahora redirigimos a /admin/login/ hasta tener nuestra propia vista de login
    return redirect("/admin/login/")
