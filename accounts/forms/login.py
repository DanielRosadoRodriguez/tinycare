from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico", max_length=254)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, min_length=8)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica estilos/UX a los widgets aquí (no en el template)
        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "type": "email",
            "placeholder": "tucorreo@dominio.com",
            "autocomplete": "email",
        })
        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "type": "password",
            "placeholder": "Tu contraseña",
            "autocomplete": "current-password",
        })

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        password = cleaned.get("password")
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise forms.ValidationError("Credenciales inválidas.")
            cleaned["user"] = user
        return cleaned
