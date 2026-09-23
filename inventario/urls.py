"""
Enrutamiento local del módulo de Inventario.
Permite delegar las direcciones web correspondientes a la gestión de productos y stock.
"""

from django.urls import path
from . import views

# Namespace para el módulo de inventario
app_name = 'inventario'

urlpatterns = [
    # Ruta principal del módulo: Dashboard administrativo
    path('', views.dashboard_inventario, name='dashboard'),
    # Ruta secundaria: Catálogo interno de productos
    path('productos/', views.lista_productos, name='lista_productos'),
]
