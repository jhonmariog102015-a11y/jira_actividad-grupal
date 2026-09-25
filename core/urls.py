"""
Configuración global de URLs para el proyecto core.
Actúa como el enrutador principal que delega el tráfico hacia las aplicaciones modulares
mediante la función include().
"""

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Panel de administración predeterminado de Django
    path('admin/', admin.site.urls),
    
    # Ruta pública raíz: Landing page para clientes y visitantes
    path('', views.home, name='home'),
    
    # Enrutamiento modular: delega las rutas hacia la aplicación 'inventario'
    path('inventario/', include('inventario.urls')),
    
    # Rutas integradas del proyecto formativo El Paso Frutería
    path('tienda/', views.tienda_fruteria, name='tienda_fruteria'),
    path('catalogo-frutas/', views.catalogo_frutas, name='catalogo_frutas'),
    
    # Vista de previsualización autenticada para evidencias del panel Django
    path('admin-preview/', views.admin_preview, name='admin_preview'),
]
