"""
Vistas generales del proyecto central (Core).
Gestiona la navegación pública y las páginas de aterrizaje principales.
"""

from django.shortcuts import render

def home(request):
    """
    Vista de la página principal (Landing Page) para clientes y usuarios generales.
    Utiliza la plantilla pública base_cliente.html.
    """
    contexto = {
        'titulo': 'Inicio | ADSO Software de Gestión',
        'nombre_empresa': 'Stratum Group & ADSO Solutions',
        'lema': 'Plataforma Integral de Control y Gestión de la Información Empresarial',
        'descripcion': 'Arquitectura modular construida con Django, motor de plantillas DTL y diseño responsivo Bootstrap 5.',
    }
    return render(request, 'home.html', contexto)
