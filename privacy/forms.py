from django import forms
from privacy.models import Consentimiento


class ConsentimientoForm(forms.ModelForm):
    """
    Formulario para gestionar consentimientos del usuario.
    """
    class Meta:
        model = Consentimiento
        fields = ['analitica', 'marketing', 'personalizacion', 'investigacion']
        widgets = {
            'analitica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'marketing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'personalizacion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'investigacion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
