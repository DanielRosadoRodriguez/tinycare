# accounts/forms/registration_specialist.py
from django import forms
from .registration_base import RegistrationBaseForm

class SpecialistRegistrationForm(RegistrationBaseForm):
    """Formulario de registro para Especialistas, con cédula profesional."""
    cedula_profesional = forms.CharField(label="Cédula profesional", max_length=32)
