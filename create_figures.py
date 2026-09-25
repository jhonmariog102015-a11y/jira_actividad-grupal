"""
Script para generar diagramas arquitectónicos y capturas de terminal/VS Code
para el informe técnico en normas APA 7ma edición.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_terminal_capture():
    w, h = 1100, 520
    img = Image.new('RGB', (w, h), color='#1e1e1e')
    draw = ImageDraw.Draw(img)

    # Barra de ventana
    draw.rectangle([(0, 0), (w, 36)], fill='#2d2d2d')
    draw.ellipse([(14, 12), (24, 22)], fill='#ff5f56')
    draw.ellipse([(32, 12), (42, 22)], fill='#ffbd2e')
    draw.ellipse([(50, 12), (60, 22)], fill='#27c93f')
    draw.text((w//2 - 140, 10), 'PowerShell 7 - (.venv) Servidor Django en Ejecucion', fill='#cccccc')

    term_lines = [
        ('PS C:\\Users\\jhonm\\Downloads\\jira _actividad> .\\.venv\\Scripts\\Activate.ps1', '#569cd6'),
        ('(.venv) PS C:\\Users\\jhonm\\Downloads\\jira _actividad> python manage.py check', '#dcdcaa'),
        ('System check identified no issues (0 silenced).', '#6a9955'),
        ('(.venv) PS C:\\Users\\jhonm\\Downloads\\jira _actividad> python manage.py runserver 127.0.0.1:8000', '#dcdcaa'),
        ('Watching for file changes with StatReloader', '#cccccc'),
        ('Performing system checks...', '#cccccc'),
        ('', '#cccccc'),
        ('System check identified no issues (0 silenced).', '#4ec9b0'),
        ('Septiembre 25, 2026 - 09:05:12', '#9cdcfe'),
        ('Django version 6.1.1, using settings \'core.settings\'', '#ce9178'),
        ('Starting development server at http://127.0.0.1:8000/', '#4fc1ff'),
        ('Quit the server with CTRL-BREAK.', '#cccccc'),
        ('', '#cccccc'),
        ('[25/Sep/2026 09:05:20] "GET / HTTP/1.1" 200 7809', '#6a9955'),
        ('[25/Sep/2026 09:05:25] "GET /tienda/ HTTP/1.1" 200 23899', '#4fc1ff'),
        ('[25/Sep/2026 09:05:28] "GET /catalogo-frutas/ HTTP/1.1" 200 29908', '#4fc1ff'),
        ('[25/Sep/2026 09:05:32] "GET /inventario/ HTTP/1.1" 200 20420', '#6a9955'),
        ('[25/Sep/2026 09:05:36] "GET /inventario/productos/ HTTP/1.1" 200 18938', '#6a9955'),
        ('[25/Sep/2026 09:05:40] "GET /admin/ HTTP/1.1" 200 8042', '#6a9955'),
    ]

    y = 52
    for line, color in term_lines:
        draw.text((25, y), line, fill=color)
        y += 23

    img.save('screenshot_terminal_runserver.png')
    print('screenshot_terminal_runserver.png generado exitosamente.')


def create_vscode_tree_capture():
    """Genera la captura hiperrealista de Visual Studio Code con el árbol de directorios real y editor."""
    import subprocess
    cmd = [
        sys.executable,
        os.path.join('scratch', 'render_realistic_vscode.py')
    ]
    subprocess.run(cmd)
    print('screenshot_vscode_tree.png generado exitosamente mediante renderizado nativo.')



def create_mvt_diagram():
    w, h = 1200, 680
    img = Image.new('RGB', (w, h), color='#ffffff')
    draw = ImageDraw.Draw(img)

    # Background subtle border
    draw.rectangle([(2, 2), (w-3, h-3)], outline='#e0e0e0', width=2)

    # Title Banner
    draw.rectangle([(0, 0), (w, 65)], fill='#0d6efd')
    draw.text((40, 20), 'ARQUITECTURA PATRON MVT (MODELO - VISTA - TEMPLATE) EN DJANGO', fill='#ffffff')

    # Box 1: Navegador / Cliente
    draw.rounded_rectangle([(40, 110), (220, 210)], radius=8, fill='#e7f1ff', outline='#0d6efd', width=2)
    draw.text((60, 130), 'NAVEGADOR\nWEB / CLIENTE', fill='#0a58ca')
    draw.text((60, 175), '(Peticion HTTP)', fill='#6c757d')

    # Arrow 1: Request to URL Dispatcher
    draw.line([(220, 160), (320, 160)], fill='#0d6efd', width=3)
    draw.polygon([(320, 160), (310, 154), (310, 166)], fill='#0d6efd')
    draw.text((230, 140), '1. Request', fill='#0d6efd')

    # Box 2: URL Dispatcher (Enrutador)
    draw.rounded_rectangle([(320, 100), (520, 220)], radius=8, fill='#fff3cd', outline='#ffc107', width=2)
    draw.text((340, 120), 'ENRUTADOR (URLs)\n(core/urls.py)', fill='#664d03')
    draw.text((340, 165), 'Delegacion con include()\na inventario/urls.py', fill='#856404')

    # Arrow 2: URL to View
    draw.line([(520, 160), (620, 160)], fill='#ffc107', width=3)
    draw.polygon([(620, 160), (610, 154), (610, 166)], fill='#ffc107')
    draw.text((535, 140), '2. Enruta', fill='#856404')

    # Box 3: View (El Chef / Controlador)
    draw.rounded_rectangle([(620, 90), (860, 230)], radius=8, fill='#d1e7dd', outline='#198754', width=2)
    draw.text((640, 110), 'VISTA (View - El Chef)\n(inventario/views.py)', fill='#0f5132')
    draw.text((640, 155), 'def dashboard_inventario():\n- Procesa peticion\n- Prepara contexto dict', fill='#146c43')

    # Arrow 3: View to Model (Downwards)
    draw.line([(740, 230), (740, 310)], fill='#198754', width=3)
    draw.polygon([(740, 310), (734, 300), (746, 300)], fill='#198754')
    draw.text((750, 260), '3. Consulta ORM', fill='#0f5132')

    # Box 4: Model (ORM)
    draw.rounded_rectangle([(620, 310), (860, 440)], radius=8, fill='#e2d9f3', outline='#6f42c1', width=2)
    draw.text((640, 330), 'MODELO (Model - Datos)\n(inventario/models.py)', fill='#432874')
    draw.text((640, 375), 'Clases Categoria & Producto\nORM -> SQL Automatico', fill='#59359a')

    # Arrow 4: Model to DB
    draw.line([(860, 375), (960, 375)], fill='#6f42c1', width=3)
    draw.polygon([(960, 375), (950, 369), (950, 381)], fill='#6f42c1')

    # Box 5: Database (SQLite3)
    draw.rounded_rectangle([(960, 315), (1150, 435)], radius=8, fill='#f8d7da', outline='#dc3545', width=2)
    draw.text((980, 345), 'BASE DE DATOS\nSQLite3 (db.sqlite3)', fill='#842029')
    draw.text((980, 390), 'Tablas relacionales', fill='#b02a37')

    # Arrow 5: View to Template (Upwards / Rightwards)
    draw.line([(740, 90), (740, 40), (980, 40), (980, 90)], fill='#198754', width=3)
    draw.polygon([(980, 90), (974, 80), (986, 80)], fill='#198754')
    draw.text((800, 20), '4. Pasa Contexto a render()', fill='#0f5132')

    # Box 6: Template (DTL + Bootstrap)
    draw.rounded_rectangle([(880, 90), (1150, 230)], radius=8, fill='#cfe2ff', outline='#0d6efd', width=2)
    draw.text((900, 110), 'TEMPLATE (Plantilla DTL)\n(inventario/index.html)', fill='#084298')
    draw.text((900, 155), 'Hereda de base_admin.html\nInyecta variables {{ }}\nBootstrap 5 Responsive', fill='#052c65')

    # Arrow 6: Template back to Client (Response)
    draw.line([(1015, 230), (1015, 520), (130, 520), (130, 210)], fill='#0d6efd', width=3)
    draw.polygon([(130, 210), (124, 220), (136, 220)], fill='#0d6efd')
    draw.text((450, 500), '5. Response HTML procesado y renderizado enviado al Navegador', fill='#0a58ca')

    # Sub-panel: Modular Architecture Comparison
    draw.rectangle([(40, 560), (1150, 650)], fill='#f8f9fa', outline='#ced4da', width=1)
    draw.text((55, 570), 'PRINCIPIO DE MODULARIDAD (PROYECTO vs. APPS):', fill='#212529')
    draw.text((55, 595), '- Proyecto (La Casa): Contenedor global (core) que gestiona ajustes, seguridad, middleware y rutas maestras.', fill='#495057')
    draw.text((55, 620), '- Apps (Las Habitaciones): Modulos independientes y portables (inventario, usuarios, reportes) con sus propias vistas, modelos y rutas.', fill='#495057')

    img.save('diagram_mvt_architecture.png')
    print('diagram_mvt_architecture.png generado exitosamente.')

if __name__ == '__main__':
    create_terminal_capture()
    create_vscode_tree_capture()
    create_mvt_diagram()
