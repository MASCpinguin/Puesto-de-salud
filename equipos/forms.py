from django import forms

from .models import Equipo


class EquipoForm(forms.ModelForm):
    """Formulario para registrar un usuario y las pruebas que solicita."""

    class Meta:
        model = Equipo
        fields = ['nombre', 'documento', 'puesto', 'microbiologia', 'bacteriologia', 'quimica']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: María Gómez'}),
            'documento': forms.TextInput(attrs={'placeholder': 'Ej: 1144000000'}),
            'microbiologia': forms.NumberInput(attrs={'min': 0, 'class': 'prueba'}),
            'bacteriologia': forms.NumberInput(attrs={'min': 0, 'class': 'prueba'}),
            'quimica': forms.NumberInput(attrs={'min': 0, 'class': 'prueba'}),
        }

    def clean_documento(self):
        documento = self.cleaned_data['documento'].strip()
        if not documento.isdigit():
            raise forms.ValidationError('El documento solo debe contener números.')
        return documento

    def clean(self):
        datos = super().clean()
        total = sum(datos.get(c) or 0 for c in ('microbiologia', 'bacteriologia', 'quimica'))
        if total < 1:
            raise forms.ValidationError('El usuario debe solicitar al menos una prueba (M ≥ 1).')
        return datos
