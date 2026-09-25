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
    with open('core/urls.py', 'r', encoding='utf-8') as f:
        core_urls_raw = f.read().strip()
    with open('inventario/urls.py', 'r', encoding='utf-8') as f:
        inv_urls_raw = f.read().strip()

    urls_snippet = f"""# 1. core/urls.py - Enrutador Maestro con Delegación y Rutas El Paso Frutería
{core_urls_raw}

# -------------------------------------------------------------
# 2. inventario/urls.py - Enrutador Local del Módulo de Inventario
{inv_urls_raw}
"""
    generate_capture(
        urls_snippet,
        PythonLexer(),
        'urls.py (core & inventario)',
        'core > urls.py ➔ inventario > urls.py',
        '🔗',
        'screenshot_code_urls.png',
        window_size='1100,720'
    )

    # 3. Capture Models (inventario/models.py)
    with open('inventario/models.py', 'r', encoding='utf-8') as f:
        models_raw = f.read().strip()

    generate_capture(
        models_raw,
        PythonLexer(),
        'models.py',
        'inventario > models.py',
        '🗄️',
        'screenshot_code_models.png',
        window_size='1100,680'
    )

    # 4. Capture Views (core/views.py & inventario/views.py)
    with open('core/views.py', 'r', encoding='utf-8') as f:
        core_views_raw = f.read().strip()
    with open('inventario/views.py', 'r', encoding='utf-8') as f:
        inv_views_raw = f.read().strip()

    views_snippet = f"""# 1. core/views.py - Vistas Públicas y Enrutamiento de El Paso Frutería
{core_views_raw}

# -------------------------------------------------------------
# 2. inventario/views.py - Vista FBV del Dashboard con ORM y Contexto
{inv_views_raw}
"""
    generate_capture(
        views_snippet,
        PythonLexer(),
        'views.py (core & inventario)',
        'core > views.py ➔ inventario > views.py',
        '⚡',
        'screenshot_code_views.png',
        window_size='1100,760'
    )

    # 5. Capture Templates (templates/home.html & templates/fruteria/tienda.html)
    template_snippet = """<!-- templates/home.html - Enlaces Canónicos a Tienda y Catálogo El Paso Frutería -->
{% extends 'base_cliente.html' %}

{% block title %}Inicio | Plataforma de Gestión ADSO{% endblock title %}

{% block content %}
<div class="row align-items-center mb-5">
    <div class="col-lg-7">
        <div class="p-4 p-md-5 bg-white rounded-3 shadow-sm border">
            <span class="badge bg-primary-subtle text-primary mb-2 px-3 py-2 fw-semibold">
                SENA - Regional Boyacá | ADSO 3321349
            </span>
            <h1 class="display-5 fw-bold text-dark mb-3">{{ nombre_empresa }}</h1>
            <p class="lead text-secondary mb-4">{{ lema }}</p>
            <p class="text-muted">{{ descripcion }}</p>
            
            <!-- Botones de Acción integrados hacia El Paso Frutería e Inventario -->
            <div class="d-flex flex-wrap gap-2 mt-4">
                <a href="/tienda/" class="btn btn-success btn-lg px-4 shadow">
                    <i class="bi bi-shop me-2"></i>Ir a Tienda El Paso
                </a>
                <a href="/catalogo-frutas/" class="btn btn-warning btn-lg px-4 shadow text-dark fw-semibold">
                    <i class="bi bi-basket me-2"></i>Ver Catálogo Frutas
                </a>
                <a href="/inventario/" class="btn btn-outline-primary btn-lg px-4">
                    <i class="bi bi-speedometer2 me-2"></i>Panel Administrativo
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
"""
    generate_capture(
        template_snippet,
        HtmlDjangoLexer(),
        'home.html (El Paso Frutería Links)',
        'templates > home.html',
        '🎨',
        'screenshot_code_templates.png',
        window_size='1100,720'
    )

if __name__ == '__main__':
    main()
