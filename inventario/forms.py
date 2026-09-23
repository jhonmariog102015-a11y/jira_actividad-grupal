"""
Formularios del módulo de Inventario.
Separa la lógica de validación de datos para la gestión segura de productos.
"""

from django import forms
from .models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    """Formulario para la creación y edición de productos con estilos Bootstrap 5."""
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Taladro percutor'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }
