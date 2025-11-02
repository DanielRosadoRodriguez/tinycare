from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # Bootstrap-friendly inputs
            css = field.widget.attrs.get("class", "")
            field.widget.attrs.update({"class": (css + " form-control").strip()})
            # Provide clearer labels in Spanish
            if name == "username":
                field.label = "Usuario"
            elif name == "first_name":
                field.label = "Nombre"
            elif name == "last_name":
                field.label = "Apellido"
            elif name == "email":
                field.label = "Correo electrónico"

    def clean_email(self):
        """Asegura que el email no esté usado por otro usuario."""
        email = self.cleaned_data.get("email")
        if not email:
            return email
        qs = User.objects.filter(email__iexact=email)
        # Excluir al usuario actual si el formulario fue instanciado con uno
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este correo ya está en uso por otro usuario.")
        return email

    def save(self, commit=True):
        """
        Sobrescribe save para sincronizar username con email.
        En este proyecto, username siempre debe ser igual al email.
        """
        user = super().save(commit=False)
        # Sincronizar username con email
        if self.cleaned_data.get("email"):
            user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
