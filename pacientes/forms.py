from django.forms import ModelForm
from .models import Paciente
from django import forms


class PacienteForm(ModelForm):
    """Form definition for paciente."""

    class Meta:
        """Meta definition for pacienteform."""
        model = Paciente
        fields = '__all__'
        widgets = {'fecha_nacimiento': forms.DateInput(attrs={'class': 'datepicker'})}
