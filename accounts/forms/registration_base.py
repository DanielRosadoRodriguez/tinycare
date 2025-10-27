# accounts/forms/registration_base.py
from django import forms

class RegistrationBaseForm(forms.Form):
    nombres = forms.CharField(label="Nombre(s)", max_length=80)
    apellido_paterno = forms.CharField(label="Apellido paterno", max_length=80)
    apellido_materno = forms.CharField(label="Apellido materno", max_length=80, required=False)

    email = forms.EmailField(label="Correo electrónico", max_length=254)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, min_length=8)
    password_confirm = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput, min_length=8)

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        pwd2 = cleaned.get("password_confirm")
        if pwd and pwd2 and pwd != pwd2:
            self.add_error("password_confirm", "Las contraseñas no coinciden.")
        return cleaned
