from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from django.forms import modelform_factory
from django.contrib.auth import get_user_model

from ..forms.profile_form import ProfileForm
from accounts.models.profile_parent import ProfileParent
from accounts.models.profile_specialist import ProfileSpecialist


@login_required
def profile_view(request):
    """View and edit profile for the current user."""
    user = request.user
    # intentar obtener el perfil (Parent primero, luego Specialist)
    profile = ProfileParent.objects.filter(user=user).first()
    profile_model = ProfileParent if profile else None
    if not profile:
        profile = ProfileSpecialist.objects.filter(user=user).first()
        profile_model = ProfileSpecialist if profile else profile_model

    # crear dinámicamente un ModelForm para el perfil si existe
    profile_form = None
    if profile_model:
        fields = ["nombres", "apellido_paterno", "apellido_materno"]
        if profile_model is ProfileSpecialist:
            fields.append("cedula_profesional")
        ProfileModelForm = modelform_factory(profile_model, fields=fields)
        # Asegurar que los widgets del form de perfil usen clases de Bootstrap
        for fname, f in ProfileModelForm.base_fields.items():
            css = f.widget.attrs.get("class", "")
            f.widget.attrs.update({"class": (css + " form-control").strip()})

    if request.method == "POST":
        user_form = ProfileForm(request.POST, instance=user)
        if profile_model:
            profile_form = ProfileModelForm(request.POST, instance=profile)
        forms_valid = user_form.is_valid() and (profile_form.is_valid() if profile_form else True)
        # Si la validación falla, comprobar explícitamente si el email enviado ya pertenece a otro usuario
        # y mostrar sólo un mensaje claro en el campo 'email' (evitar duplicados/confusión).
        if not forms_valid:
            provided_email = request.POST.get("email", "").strip()
            if provided_email:
                User = get_user_model()
                if User.objects.filter(email__iexact=provided_email).exclude(pk=user.pk).exists():
                    # Añadir error sólo si no existe ya (evita duplicado)
                    if "email" not in user_form.errors:
                        user_form.add_error("email", "Este correo ya está registrado en otra cuenta.")
                    # eliminar posible error genérico sobre username para no confundir
                    if "username" in user_form.errors:
                        user_form.errors.pop("username", None)
        if forms_valid:
            # sincronizar username con email si el correo fue cambiado
            new_email = user_form.cleaned_data.get("email")
            if new_email and new_email != user.email:
                user_form.instance.username = new_email
            user_form.save()
            if profile_form:
                profile_obj = profile_form.save(commit=False)
                # si por alguna razón no existía profile (crear), asignar user
                if not profile_obj.pk:
                    profile_obj.user = user
                profile_obj.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("accounts:profile")
    else:
        user_form = ProfileForm(instance=user)
        if profile_model:
            profile_form = ProfileModelForm(instance=profile)

    # determinar tipo de cuenta para la UI
    if profile and isinstance(profile, ProfileParent):
        account_type = "Padre/Madre"
    elif profile and isinstance(profile, ProfileSpecialist):
        account_type = "Especialista"
    else:
        account_type = "Sin perfil"

    return render(request, "accounts/profile.html", {"user": user, "user_form": user_form, "profile_form": profile_form, "profile": profile, "account_type": account_type})
