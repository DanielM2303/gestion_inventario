from django.forms import ModelForm
from apps.categorias.models import Categoriaarticulos

# Clase Formulario Categoria
class CategoriaForm(ModelForm):
    # Inicialización del formulario
    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        
        # Personalización de los widgets
        self.fields['descripcion_categoriaarticulo'].widget.attrs.update({'placeholder': 'Ingresa el nombre'})

    # Opciones adicionales
    class Meta:
        model = Categoriaarticulos
        fields = ['descripcion_categoriaarticulo']
