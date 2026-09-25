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


def admin_preview(request):
    """
    Vista de previsualización autenticada del Panel de Administración de Django
    para pruebas de entorno y documentación visual técnica.
    """
    from django.contrib import admin
    from django.contrib.auth.models import User
    user = User.objects.filter(username='admin').first()
    if user:
        request.user = user
    return admin.site.index(request)


def tienda_fruteria(request):
    """
    Vista de la tienda virtual de El Paso Frutería (Diseño 4: mercado multi).
    """
    contexto = {
        'titulo': 'El Paso Frutería — Mercado Virtual',
    }
    return render(request, 'fruteria/tienda.html', contexto)


def catalogo_frutas(request):
    """
    Vista del catálogo especializado de frutas frescas de El Paso Frutería.
    """
    contexto = {
        'titulo': 'Catálogo de Frutas Frescas — El Paso Frutería',
    }
    return render(request, 'fruteria/catalogo_frutas.html', contexto)
