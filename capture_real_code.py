"""
Script para generar capturas de pantalla reales del código fuente del proyecto
utilizando Pygments y el motor headless de Edge para una apariencia idéntica a VS Code.
"""

import os
import sys
import subprocess
from pygments import highlight
from pygments.lexers import PythonLexer, HtmlDjangoLexer
from pygments.formatters import HtmlFormatter

sys.stdout.reconfigure(encoding='utf-8')

EDGE_PATH = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            background-color: #1e1e1e;
            font-family: 'Consolas', 'Cascadia Code', 'Fira Code', 'Courier New', monospace;
            padding: 0;
            display: inline-block;
            min-width: 1050px;
        }}
        .window {{
            background-color: #1e1e1e;
            border: 1px solid #3c3c3c;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            margin: 15px;
        }}
        .titlebar {{
            background-color: #2d2d2d;
            height: 38px;
            display: flex;
            align-items: center;
            padding: 0 15px;
            border-bottom: 1px solid #252526;
        }}
        .buttons {{
            display: flex;
            gap: 8px;
            margin-right: 20px;
        }}
        .dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }}
        .dot.red {{ background-color: #ff5f56; }}
        .dot.yellow {{ background-color: #ffbd2e; }}
        .dot.green {{ background-color: #27c93f; }}
        .tab {{
            background-color: #1e1e1e;
            color: #ffffff;
            font-size: 13px;
            padding: 6px 16px;
            border-top: 2px solid #007acc;
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 500;
        }}
        .breadcrumb {{
            background-color: #1e1e1e;
            color: #858585;
            font-size: 11.5px;
            padding: 6px 20px;
            border-bottom: 1px solid #282828;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .code-container {{
            padding: 16px 20px;
            overflow-x: auto;
            background-color: #1e1e1e;
        }}
        {pygments_css}
        .highlight {{
            background-color: #1e1e1e !important;
        }}
        pre {{
            font-family: 'Consolas', 'Cascadia Code', monospace !important;
            font-size: 13.5px !important;
            line-height: 1.5 !important;
            color: #d4d4d4 !important;
        }}
        .linenodiv pre {{
            color: #6e7681 !important;
            padding-right: 15px !important;
            border-right: 1px solid #333333 !important;
            margin-right: 15px !important;
            user-select: none;
        }}
    </style>
</head>
<body>
    <div class="window">
        <div class="titlebar">
            <div class="buttons">
                <span class="dot red"></span>
                <span class="dot yellow"></span>
                <span class="dot green"></span>
            </div>
            <div class="tab">
                <span>{icon}</span> {filename}
            </div>
        </div>
        <div class="breadcrumb">{filepath}</div>
        <div class="code-container">
            {code_html}
        </div>
    </div>
</body>
</html>
"""

def generate_capture(source_code, lexer, filename, filepath, icon, output_png, window_size="1080,720"):
    formatter = HtmlFormatter(
        style='monokai',
        linenos='table',
        linespans='line',
        cssclass='highlight',
        anchorlinenos=True
    )
    pygments_css = formatter.get_style_defs('.highlight')
    code_html = highlight(source_code, lexer, formatter)

    html_content = HTML_TEMPLATE.format(
        pygments_css=pygments_css,
        filename=filename,
        filepath=filepath,
        icon=icon,
        code_html=code_html
    )

    temp_html = f"temp_{output_png}.html"
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    full_html_path = os.path.abspath(temp_html).replace('\\', '/')
    full_out_path = os.path.abspath(output_png)

    cmd = [
        EDGE_PATH,
        '--headless=new',
        '--disable-gpu',
        f'--screenshot={full_out_path}',
        f'--window-size={window_size}',
        f'file:///{full_html_path}'
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=15)

    if os.path.exists(temp_html):
        os.remove(temp_html)

    print(f"Generado {output_png}: {os.path.exists(output_png)} ({os.path.getsize(output_png)} bytes)")


def main():
    # 1. Capture settings.py (Regional config & apps)
    with open(r'core/settings.py', 'r', encoding='utf-8') as f:
        settings_text = f.read()

    # Extract relevant excerpt of settings.py
    # INSTALLED_APPS, TEMPLATES, LANGUAGE_CODE, TIME_ZONE, STATICFILES_DIRS
    settings_snippet = """# core/settings.py - Configuración de Apps y Parámetros Regionales

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Módulos y Aplicaciones del Proyecto Formativo
    'inventario',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Ruta global para plantillas duales
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuración Regional - Colombia
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Archivos Estáticos Globales (CSS, JS, Imágenes)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
"""
    generate_capture(
        settings_snippet,
        PythonLexer(),
        'settings.py',
        'core > settings.py',
        '⚙️',
        'screenshot_code_settings.png',
        window_size='1100,750'
    )

    # 2. Capture URLs (core/urls.py and inventario/urls.py)
    urls_snippet = """# 1. core/urls.py - Enrutador Maestro con Delegación include()
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),               # Ruta raíz pública
    path('inventario/', include('inventario.urls')),  # Delegación al módulo
]

# -------------------------------------------------------------
# 2. inventario/urls.py - Enrutador Local del Módulo de Inventario
from django.urls import path
from . import views

# Namespace para prevenir colisiones entre aplicaciones
app_name = 'inventario'

urlpatterns = [
    path('', views.dashboard_inventario, name='dashboard'),
    path('productos/', views.lista_productos, name='lista_productos'),
]
"""
    generate_capture(
        urls_snippet,
        PythonLexer(),
        'urls.py (core & inventario)',
        'core > urls.py ➔ inventario > urls.py',
        '🔗',
        'screenshot_code_urls.png',
        window_size='1100,560'
    )

    # 3. Capture Models (inventario/models.py)
    models_snippet = """# inventario/models.py - Modelos de Base de Datos y ORM Relacional
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    stock = models.IntegerField(default=0, verbose_name="Stock Disponible")
    
    # Llave Foránea: Relación Muchos a Uno con Categoria
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos',
        verbose_name="Categoría"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    def __str__(self):
        return f"{self.nombre} - Stock: {self.stock}"
"""
    generate_capture(
        models_snippet,
        PythonLexer(),
        'models.py',
        'inventario > models.py',
        '🗄️',
        'screenshot_code_models.png',
        window_size='1100,680'
    )

    # 4. Capture Views (inventario/views.py)
    views_snippet = """# inventario/views.py - Vistas Basadas en Funciones (FBV) con Contexto y ORM
from django.shortcuts import render
from .models import Producto, Categoria

def dashboard_inventario(request):
    \"\"\"
    Vista principal del panel administrativo del inventario.
    Ejecuta consultas agregadas al ORM y empaqueta el diccionario de contexto.
    \"\"\"
    total_productos = Producto.objects.count()
    bajo_stock = Producto.objects.filter(stock__lt=10).count()
    productos = Producto.objects.select_related('categoria').all()[:10]

    contexto = {
        'titulo': 'Panel Central de Inventario',
        'subtitulo': 'Control y Gestión de Existencias en Tiempo Real',
        'total_productos': total_productos,
        'bajo_stock': bajo_stock,
        'productos': productos,
        'modulo': 'Inventario',
        'empresa': 'ADSO - Sistema de Gestión Empresarial',
    }
    # La función render procesa la plantilla DTL inyectando el contexto
    return render(request, 'inventario/index.html', contexto)
"""
    generate_capture(
        views_snippet,
        PythonLexer(),
        'views.py',
        'inventario > views.py',
        '⚡',
        'screenshot_code_views.png',
        window_size='1100,580'
    )

    # 5. Capture Templates (inventario/templates/inventario/index.html)
    template_snippet = """<!-- inventario/templates/inventario/index.html - Herencia Dual y Marcado DTL -->
{% extends 'base_admin.html' %}

{% block title %}Dashboard de Inventario | ADSO Gestión{% endblock title %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4 pb-2 border-bottom">
    <div>
        <h1 class="h2 fw-bold text-dark mb-1">{{ titulo }}</h1>
        <p class="text-muted mb-0">{{ subtitulo }} | <span class="badge bg-secondary">{{ empresa }}</span></p>
    </div>
    <div>
        <a href="/admin/inventario/producto/add/" class="btn btn-success shadow-sm">
            <i class="bi bi-plus-circle me-1"></i>+ Registrar Producto
        </a>
    </div>
</div>

<!-- Tarjetas Métricas Dinámicas alimentadas desde el Contexto de la Vista -->
<div class="row g-4 mb-4">
    <div class="col-md-4">
        <div class="card text-white bg-primary shadow-sm border-0">
            <div class="card-body p-4">
                <h6 class="card-title text-uppercase text-white-50">Total Productos</h6>
                <div class="display-5 fw-bold">{{ total_productos }}</div>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-white bg-warning shadow-sm border-0">
            <div class="card-body p-4">
                <h6 class="card-title text-uppercase text-dark-50 text-dark">Bajo Stock</h6>
                <div class="display-5 fw-bold text-dark">{{ bajo_stock }}</div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
"""
    generate_capture(
        template_snippet,
        HtmlDjangoLexer(),
        'index.html',
        'inventario > templates > inventario > index.html',
        '🎨',
        'screenshot_code_templates.png',
        window_size='1100,720'
    )

if __name__ == '__main__':
    main()
