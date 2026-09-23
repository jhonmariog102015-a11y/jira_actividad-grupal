"""
Configuración del Panel Administrativo de Django para la App Inventario.
"""

from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'stock', 'categoria', 'fecha_registro')
    list_filter = ('categoria', 'fecha_registro')
    search_fields = ('nombre', 'categoria__nombre')
    list_editable = ('precio', 'stock')
