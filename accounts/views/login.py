from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from accounts.forms.login import LoginForm

def login_view(request):
    """
    GET: muestra formulario de login
    POST: valida credenciales y redirige a la página de saludo
    """
    if request.method == "GET":
        return render(request, "accounts/login.html", {"form": LoginForm()})

    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(request, "accounts/login.html", {"form": form}, status=400)

    user = form.cleaned_data["user"]
    auth_login(request, user)
    return redirect("accounts:greet")
