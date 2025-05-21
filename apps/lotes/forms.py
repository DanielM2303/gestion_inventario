from django import forms
from apps.lotes.models import Lotes
from datetime import datetime, timedelta

# Clase Formulario Lote
class LotesForm(forms.ModelForm):
    # Opciones adicionales
    class Meta:
        model = Lotes
        fields = ['numero_lote', 'fecha_fabricacion', 'fecha_caducidad', 'cantidad']
        widgets = {
            'fecha_fabricacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_caducidad': forms.DateInput(attrs={'readonly': 'readonly', 'type': 'date', 'style': 'cursor: not-allowed;'}),
            'cantidad': forms.NumberInput(attrs={'readonly': 'readonly', 'style': 'cursor: not-allowed;'}),
        }

    # Inicialización del formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalización de widgets
        self.fields['numero_lote'].widget.attrs.update({'placeholder': 'Ingresa el número de lote'})

        # Configuración de fechas
        if self.instance:
            if self.instance.fecha_fabricacion:
                self.initial['fecha_fabricacion'] = self.instance.fecha_fabricacion.strftime('%Y-%m-%d')
        if self.instance: 
            if self.instance.fecha_caducidad:
                self.initial['fecha_caducidad'] = self.instance.fecha_caducidad.strftime('%Y-%m-%d')

        # Limitar fecha_fabricacion según fecha_caducidad
        if self.instance.fecha_caducidad:
            fecha_max = (datetime.strptime(self.initial['fecha_caducidad'], '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
            self.fields['fecha_fabricacion'].widget = forms.DateInput(
                attrs={'type': 'date', 'max': fecha_max, 'class': 'form-control'}
            )
            