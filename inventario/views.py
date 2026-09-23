"""
Vistas del Módulo de Inventario (Function-Based Views - FBV).
Actúa como la capa lógica que procesa la petición HTTP, interactúa con el ORM
y ensambla el contexto con la plantilla HTML correspondiente.
"""

from django.shortcuts import render
from .models import Producto, Categoria

def dashboard_inventario(request):
    """
    Vista principal del dashboard administrativo del inventario.
    Calcula métricas clave de existencias y despacha el contexto al template index.html.
    """
    try:
        total_productos = Producto.objects.count()
        bajo_stock = Producto.objects.filter(stock__lt=10).count()
        productos = Producto.objects.select_related('categoria').all()[:10]
    except Exception:
        total_productos = 0
        bajo_stock = 0
        productos = []

    contexto = {
        'titulo': 'Panel Central de Inventario',
        'subtitulo': 'Control y Gestión de Existencias en Tiempo Real',
        'total_productos': total_productos,
        'bajo_stock': bajo_stock,
        'productos': productos,
        'modulo': 'Inventario',
        'empresa': 'ADSO - Sistema de Gestión Empresarial',
    }
    return render(request, 'inventario/index.html', contexto)


def lista_productos(request):
    """
    Vista de catálogo detallado de productos.
    """
    try:
        productos = Producto.objects.select_related('categoria').all()
    except Exception:
        productos = []

    contexto = {
        'titulo': 'Catálogo General de Productos',
        'subtitulo': 'Listado completo de existencias registradas',
        'productos': productos,
    }
    return render(request, 'inventario/productos/lista.html', contexto)
