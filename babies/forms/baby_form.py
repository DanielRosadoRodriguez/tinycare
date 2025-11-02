"""
Formulario para crear y editar bebés.
"""

from django import forms
from babies.models import Baby


class BabyForm(forms.ModelForm):
    """
    Formulario ModelForm para crear/editar información de bebés.
    Aplica estilos Bootstrap a todos los campos automáticamente.
    """

    class Meta:
        model = Baby
        fields = [
            "nombre",
            "fecha_nacimiento",
            "sexo",
            "peso",
            "alergias",
            "condiciones_salud",
        ]
        widgets = {
            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "alergias": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "condiciones_salud": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clase Bootstrap a todos los campos
        for field_name, field in self.fields.items():
            css_class = field.widget.attrs.get("class", "")
            if "form-control" not in css_class:
                field.widget.attrs.update(
                    {"class": (css_class + " form-control").strip()}
                )

        # Personalizar labels en español
        self.fields["nombre"].label = "Nombre del bebé"
        self.fields["fecha_nacimiento"].label = "Fecha de nacimiento"
        self.fields["sexo"].label = "Sexo"
        self.fields["peso"].label = "Peso (kg)"
        self.fields["peso"].help_text = "Peso actual del bebé en kilogramos (opcional)"
        self.fields["alergias"].label = "Alergias"
        self.fields["alergias"].help_text = (
            "Registra alergias conocidas del bebé (opcional)"
        )
        self.fields["condiciones_salud"].label = "Condiciones de salud"
        self.fields["condiciones_salud"].help_text = (
            "Condiciones médicas, enfermedades crónicas, etc. (opcional)"
        )
