"""
Generador del Informe Técnico en PDF bajo Normas APA 7.ª Edición
Actividad: "Arquitectura Base, Enrutamiento y Plantillas" (Guía G-02)
Programa: Análisis y Desarrollo de Software (ADSO) - SENA Regional Boyacá
Autores (Equipo GAES): Jhon Mario Guamanzar Sierra, Juan Carlos Merchán, Jhon Exander Gutiérrez Moreno
Instructor: Antony Reynel Botello Herrera
INCLUYE CAPTURAS REALES DEL CÓDIGO FUENTE DEL PROYECTO
"""

import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, Flowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

# Registro de páginas dinámico para la Tabla de Contenido y Listas
PAGE_REGISTRY = {}

class PageBookmark(Flowable):
    def __init__(self, key):
        super().__init__()
        self.key = key
        self.width = 0
        self.height = 0

    def draw(self):
        PAGE_REGISTRY[self.key] = self.canv._pageNumber


class APANumberedCanvas(canvas.Canvas):
    """
    Canvas personalizado para aplicar la numeración de páginas en el encabezado
    superior derecho según el estándar de Normas APA 7.ª edición.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Times-Roman", 10)
        self.setFillColor(colors.HexColor("#222222"))
        self.drawRightString(612 - 72, 792 - 45, str(self._pageNumber))
        self.restoreState()


def get_apa_styles():
    styles = getSampleStyleSheet()

    # Portada
    styles.add(ParagraphStyle(
        name='APAPortadaTitulo',
        fontName='Times-Bold',
        fontSize=15,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#000000'),
        spaceAfter=15
    ))
    styles.add(ParagraphStyle(
        name='APAPortadaSubtitulo',
        fontName='Times-Roman',
        fontSize=12,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#333333'),
        spaceAfter=30
    ))
    styles.add(ParagraphStyle(
        name='APAPortadaMeta',
        fontName='Times-Roman',
        fontSize=11,
        leading=19,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#111111')
    ))

    # Títulos y Encabezados APA 7
    styles.add(ParagraphStyle(
        name='APANivel1',
        fontName='Times-Bold',
        fontSize=13,
        leading=18,
        alignment=TA_CENTER,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='APANivel2',
        fontName='Times-Bold',
        fontSize=11.5,
        leading=16,
        alignment=TA_LEFT,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='APANivel3',
        fontName='Times-BoldItalic',
        fontSize=10.5,
        leading=15,
        alignment=TA_LEFT,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    ))

    # Párrafos de Cuerpo de Texto
    styles.add(ParagraphStyle(
        name='APABody',
        fontName='Times-Roman',
        fontSize=10,
        leading=14.5,
        alignment=TA_JUSTIFY,
        firstLineIndent=20,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='APABodyNoIndent',
        fontName='Times-Roman',
        fontSize=10,
        leading=14.5,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    ))

    # Resumen
    styles.add(ParagraphStyle(
        name='APAResumenTexto',
        fontName='Times-Roman',
        fontSize=10,
        leading=15,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name='APAPalabrasClave',
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
        firstLineIndent=20
    ))

    # Tablas y Figuras
    styles.add(ParagraphStyle(
        name='APATablaFiguraNum',
        fontName='Times-Bold',
        fontSize=9.5,
        leading=12,
        alignment=TA_LEFT,
        spaceAfter=2,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='APATablaFiguraTitulo',
        fontName='Times-Italic',
        fontSize=9.5,
        leading=13,
        alignment=TA_LEFT,
        spaceAfter=5,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='APATablaFiguraNota',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        alignment=TA_JUSTIFY,
        spaceBefore=4,
        spaceAfter=10
    ))

    # Celdas de Tabla
    styles.add(ParagraphStyle(
        name='APATableHeader',
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#000000')
    ))
    styles.add(ParagraphStyle(
        name='APATableCell',
        fontName='Times-Roman',
        fontSize=8,
        leading=10.5,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#222222')
    ))
    styles.add(ParagraphStyle(
        name='APATableCellCode',
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#0f5132')
    ))

    # Bloques de Código
    styles.add(ParagraphStyle(
        name='APACodeBlock',
        fontName='Courier',
        fontSize=7.8,
        leading=10.5,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#212529'),
        spaceBefore=3,
        spaceAfter=5
    ))

    # Tabla de contenido
    styles.add(ParagraphStyle(
        name='APATOCItem',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=14,
        alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        name='APATOCItemBold',
        fontName='Times-Bold',
        fontSize=9.5,
        leading=14,
        alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        name='APATOCPage',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=14,
        alignment=TA_RIGHT
    ))

    # Referencias (Sangría francesa)
    styles.add(ParagraphStyle(
        name='APAReferencia',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        alignment=TA_LEFT,
        leftIndent=24,
        firstLineIndent=-24,
        spaceAfter=7
    ))

    return styles


def build_table_of_contents_elements(styles):
    """Construye las filas de la Tabla de Contenido basándose en el PAGE_REGISTRY dinámico."""
    toc_data = [
        ("Resumen", PAGE_REGISTRY.get('resumen', 4), False),
        ("Introducción", PAGE_REGISTRY.get('intro', 5), False),
        ("Capítulo I: Actividades de Reflexión Inicial (Actividad 3.1)", PAGE_REGISTRY.get('cap1', 6), True),
        ("    Importancia de la Modularidad frente a la Estructura Monolítica", PAGE_REGISTRY.get('sec1_1', 6), False),
        ("    Análisis de Resiliencia y Tolerancia a Fallos del Sistema", PAGE_REGISTRY.get('sec1_2', 7), False),
        ("Capítulo II: Contextualización y Fundamentos Técnicos (Actividad 3.2)", PAGE_REGISTRY.get('cap2', 8), True),
        ("    Lectura Técnica: Fundamentos de Django y Filosofía de Diseño", PAGE_REGISTRY.get('sec2_1', 8), False),
        ("    Diferenciación Conceptual: Proyecto (La Casa) vs. App (Las Habitaciones)", PAGE_REGISTRY.get('sec2_2', 9), False),
        ("    Patrón de Arquitectura MVT (Modelo - Vista - Template)", PAGE_REGISTRY.get('sec2_3', 10), False),
        ("    Comparativa Técnica: Vistas Basadas en Funciones (FBV) vs. Clases (CBV)", PAGE_REGISTRY.get('sec2_4', 11), False),
        ("    El Puente de Comunicación: El Diccionario de Contexto y el Motor DTL", PAGE_REGISTRY.get('sec2_5', 12), False),
        ("Capítulo III: Apropiación del Conocimiento - Implementación Práctica (Actividad 3.3)", PAGE_REGISTRY.get('cap3', 14), True),
        ("    Aislamiento Profesional: Creación del Entorno Virtual (VENV)", PAGE_REGISTRY.get('sec3_1', 14), False),
        ("    Inicialización del Proyecto Django con Arquitectura Limpia", PAGE_REGISTRY.get('sec3_2', 14), False),
        ("    Configuración Regional y Directorios Globales en settings.py", PAGE_REGISTRY.get('sec3_3', 15), False),
        ("    Creación y Registro de la Primera Aplicación Modular (inventario)", PAGE_REGISTRY.get('sec3_4', 16), False),
        ("    Estructura Interna del Módulo y Namespacing de Plantillas", PAGE_REGISTRY.get('sec3_5', 16), False),
        ("    Enrutamiento Desacoplado mediante include() en core/urls.py", PAGE_REGISTRY.get('sec3_6', 17), False),
        ("    Lógica del Controlador y Diccionario de Contexto en views.py", PAGE_REGISTRY.get('sec3_7', 18), False),
        ("    Modelado de Datos Relacional y Persistencia con el ORM", PAGE_REGISTRY.get('sec3_8', 19), False),
        ("    Arquitectura Visual con Herencia Dual de Plantillas y Bootstrap 5", PAGE_REGISTRY.get('sec3_9', 20), False),
        ("Capítulo IV: Transferencia del Conocimiento - Prototipo y Evidencias (Actividad 3.4)", PAGE_REGISTRY.get('cap4', 21), True),
        ("    Puesta en Marcha y Verificación del Servidor Local", PAGE_REGISTRY.get('sec4_1', 21), False),
        ("    Evidencias Gráficas de Navegación Pública y Administrativa", PAGE_REGISTRY.get('sec4_2', 22), False),
        ("    Integración del Proyecto Formativo: Tienda Virtual y Catálogo de Frutas ('El Paso Frutería')", PAGE_REGISTRY.get('sec4_3', 23), False),
        ("    Catálogo Interactivo y Filtrado Dinámico de Productos Frutícolas", PAGE_REGISTRY.get('sec4_4', 24), False),
        ("    Gestión Administrativa del Inventario de Productos Frutícolas", PAGE_REGISTRY.get('sec4_5', 25), False),
        ("    Repositorio Oficial en GitHub y Control de Versiones Git", PAGE_REGISTRY.get('sec4_6', 26), False),
        ("    Criterios de Evaluación y Lista de Chequeo de la Guía G-02", PAGE_REGISTRY.get('sec4_7', 27), False),
        ("Conclusiones", PAGE_REGISTRY.get('conclusiones', 27), False),
        ("Referencias Bibliográficas", PAGE_REGISTRY.get('referencias', 28), False),
    ]

    table_rows = []
    for title, page_num, is_bold in toc_data:
        style_t = styles['APATOCItemBold'] if is_bold else styles['APATOCItem']
        table_rows.append([
            Paragraph(title, style_t),
            Paragraph(str(page_num), styles['APATOCPage'])
        ])

    toc_table = Table(table_rows, colWidths=[410, 58])
    toc_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    return toc_table


def build_list_of_tables_figures(styles):
    """Construye las listas de tablas y figuras con páginas dinámicas."""
    tables_data = [
        ("Tabla 1. Matriz Comparativa entre el Patrón MVT y el Patrón MVC Clásico", PAGE_REGISTRY.get('tab1', 10)),
        ("Tabla 2. Comparativa Técnica: Vistas Basadas en Funciones (FBV) vs. Clases (CBV)", PAGE_REGISTRY.get('tab2', 11)),
        ("Tabla 3. Herramientas y Sintaxis Esencial del Django Template Language (DTL)", PAGE_REGISTRY.get('tab3', 12)),
        ("Tabla 4. Filtros DTL más Utilizados en el Proyecto Formativo", PAGE_REGISTRY.get('tab4', 13)),
        ("Tabla 5. Matriz de Criterios de Evaluación de la Guía de Aprendizaje G-02", PAGE_REGISTRY.get('tab5', 27)),
    ]

    figures_data = [
        ("Figura 1. Diagrama de Flujo y Arquitectura del Patrón MVT en Django", PAGE_REGISTRY.get('fig1', 10)),
        ("Figura 2. Código Fuente Real: Configuración Regional y Módulos en core/settings.py", PAGE_REGISTRY.get('fig2', 15)),
        ("Figura 3. Código Fuente Real: Enrutamiento Modular Desacoplado con include()", PAGE_REGISTRY.get('fig3', 17)),
        ("Figura 4. Código Fuente Real: Vista Controladora e Inyección de Contexto en views.py", PAGE_REGISTRY.get('fig4', 18)),
        ("Figura 5. Código Fuente Real: Modelos Relacionales y Persistencia ORM en models.py", PAGE_REGISTRY.get('fig5', 19)),
        ("Figura 6. Código Fuente Real: Plantilla DTL con Herencia Dual en index.html", PAGE_REGISTRY.get('fig6', 20)),
        ("Figura 7. Consola Terminal con Entorno Virtual (.venv) y Servidor Django Activo", PAGE_REGISTRY.get('fig7', 21)),
        ("Figura 8. Interfaz Pública de Usuario basada en base_cliente.html y Bootstrap 5", PAGE_REGISTRY.get('fig8', 22)),
        ("Figura 9. Interfaz Comercial de la Tienda de Frutas ('El Paso Frutería') en /tienda/", PAGE_REGISTRY.get('fig9', 23)),
        ("Figura 10. Catálogo Interactivo y Filtrado de Frutas por Categoría en /catalogo-frutas/", PAGE_REGISTRY.get('fig10', 24)),
        ("Figura 11. Dashboard Administrativo del Módulo de Inventario con Stock Frutícola", PAGE_REGISTRY.get('fig11', 25)),
        ("Figura 12. Catálogo de Existencias con Namespacing de Plantillas en Django", PAGE_REGISTRY.get('fig12', 25)),
        ("Figura 13. Panel Administrativo Nativo de Django con Modelos Registrados", PAGE_REGISTRY.get('fig13', 26)),
    ]

    t_rows = []
    for title, page_num in tables_data:
        t_rows.append([Paragraph(title, styles['APATOCItem']), Paragraph(str(page_num), styles['APATOCPage'])])
    t_table = Table(t_rows, colWidths=[410, 58])
    t_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    f_rows = []
    for title, page_num in figures_data:
        f_rows.append([Paragraph(title, styles['APATOCItem']), Paragraph(str(page_num), styles['APATOCPage'])])
    f_table = Table(f_rows, colWidths=[410, 58])
    f_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    return t_table, f_table


def create_apa_table(num_str, title_str, headers, data, col_widths, note_str, styles, is_code_col=None):
    """Crea una tabla con formato estricto APA 7ma edición (3 líneas horizontales, sin verticales)."""
    elements = []
    elements.append(Paragraph(num_str, styles['APATablaFiguraNum']))
    elements.append(Paragraph(title_str, styles['APATablaFiguraTitulo']))

    table_data = []
    header_row = [Paragraph(h, styles['APATableHeader']) for h in headers]
    table_data.append(header_row)

    for row in data:
        row_cells = []
        for c_idx, cell in enumerate(row):
            if is_code_col and c_idx in is_code_col:
                row_cells.append(Paragraph(str(cell), styles['APATableCellCode']))
            else:
                row_cells.append(Paragraph(str(cell), styles['APATableCell']))
        table_data.append(row_cells)

    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.2, colors.HexColor('#111111')),
        ('LINEBELOW', (0, 0), (-1, 0), 1.0, colors.HexColor('#111111')),
        ('LINEBELOW', (0, -1), (-1, -1), 1.2, colors.HexColor('#111111')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t)
    elements.append(Paragraph(f"<i>Nota.</i> {note_str}", styles['APATablaFiguraNota']))
    return elements


def create_apa_figure(num_str, title_str, image_path, target_width, target_height, note_str, styles):
    """Crea un bloque de figura con formato estricto APA 7ma edición."""
    elements = []
    elements.append(Paragraph(num_str, styles['APATablaFiguraNum']))
    elements.append(Paragraph(title_str, styles['APATablaFiguraTitulo']))
    if os.path.exists(image_path):
        elements.append(Image(image_path, width=target_width, height=target_height))
    else:
        elements.append(Paragraph(f"[Imagen no encontrada: {image_path}]", styles['APABody']))
    elements.append(Paragraph(f"<i>Nota.</i> {note_str}", styles['APATablaFiguraNota']))
    return elements


def generate_pdf_story(styles):
    story = []

    # ==========================================
    # PÁGINA 1: PORTADA ESTUDIANTIL APA 7
    # ==========================================
    story.append(Spacer(1, 80))
    story.append(Paragraph("Informe Técnico: Arquitectura Base, Enrutamiento Modular y Sistema Dual de Plantillas en Django", styles['APAPortadaTitulo']))
    story.append(Paragraph("Solución Técnica y Metodológica de la Guía de Aprendizaje G-02<br/>Fase de Ejecución - Proyecto Formativo", styles['APAPortadaSubtitulo']))
    story.append(Spacer(1, 40))
    story.append(Paragraph(
        "<b>Autores (Equipo de Desarrollo GAES):</b><br/>"
        "Jhon Mario Guamanzar Sierra<br/>"
        "Juan Carlos Merchán<br/>"
        "Jhon Exander Gutiérrez Moreno<br/><br/>"
        "<b>Servicio Nacional de Aprendizaje (SENA)</b><br/>"
        "Centro Minero - Regional Boyacá<br/>"
        "Programa: Análisis y Desarrollo de Software (ADSO)<br/>"
        "Ficha de Caracterización: 3321349<br/><br/>"
        "<b>Instructor Técnico: Antony Reynel Botello Herrera</b><br/><br/>"
        "Septiembre de 2026",
        styles['APAPortadaMeta']
    ))
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 2: TABLA DE CONTENIDO
    # ==========================================
    story.append(PageBookmark('toc'))
    story.append(Paragraph("Tabla de Contenido", styles['APANivel1']))
    story.append(Spacer(1, 10))
    story.append(build_table_of_contents_elements(styles))
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 3: LISTA DE TABLAS Y LISTA DE FIGURAS
    # ==========================================
    story.append(PageBookmark('listas'))
    story.append(Paragraph("Lista de Tablas", styles['APANivel1']))
    story.append(Spacer(1, 8))
    t_tab, f_tab = build_list_of_tables_figures(styles)
    story.append(t_tab)
    story.append(Spacer(1, 16))
    story.append(Paragraph("Lista de Figuras", styles['APANivel1']))
    story.append(Spacer(1, 8))
    story.append(f_tab)
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 4: RESUMEN Y PALABRAS CLAVE
    # ==========================================
    story.append(PageBookmark('resumen'))
    story.append(Paragraph("Resumen", styles['APANivel1']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "El presente informe técnico documenta la planeación, estructuración e implementación de la arquitectura "
        "base de software para el aplicativo web institucional de control y gestión de la información, en cumplimiento "
        "de las directrices pedagógicas de la Guía de Aprendizaje G-02 del programa Análisis y Desarrollo de Software (ADSO) "
        "en el Servicio Nacional de Aprendizaje [SENA]. El proyecto técnico fue materializado empleando el framework de alto "
        "nivel Django (versión 6.1.1) sobre el lenguaje de programación Python (versión 3.14.x) en el entorno de desarrollo "
        "Visual Studio Code. En primer término, se analiza la justificación de la modularidad empresarial y la resiliencia sistémica "
        "frente a esquemas monolíticos no estructurados. Seguidamente, se desarrolla el marco conceptual comparativo del patrón "
        "arquitectónico Modelo-Vista-Template (MVT), la diferenciación entre Proyecto y Aplicación (App), y las ventajas de las "
        "Vistas Basadas en Funciones (FBV) y el motor Django Template Language (DTL). En la fase de apropiación práctica, se documentan "
        "las <b>capturas de pantalla reales del código fuente desarrollado</b>: la configuración de entornos virtuales aislados (.venv), "
        "la parametrización regional para Colombia (es-co, America/Bogota) en core/settings.py, la estructuración modular desacoplada "
        "mediante la función include() en core/urls.py e inventario/urls.py, el modelado relacional ORM en inventario/models.py, "
        "la lógica del controlador en inventario/views.py y la construcción visual con herencia dual de plantillas (base_cliente.html y base_admin.html) "
        "con Bootstrap 5. Asimismo, se documenta la integración de los componentes visuales del proyecto formativo <b>'El Paso Frutería'</b> "
        "(tienda virtual navegable y catálogo interactivo de frutas con filtrado reactivo) mediante el subsistema de archivos estáticos y plantillas DTL. "
        "Finalmente, se presentan las evidencias de ejecución del prototipo funcional en servidor local y el enlace de control de versiones al repositorio oficial en GitHub.",
        styles['APAResumenTexto']
    ))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<b>Palabras clave:</b> Django, arquitectura MVT, modularidad, código fuente real, entorno virtual, herencia dual, DTL, "
        "Bootstrap 5, El Paso Frutería, catálogo interactivo, enrutamiento, resiliencia de software, ADSO.",
        styles['APAPalabrasClave']
    ))
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 5: INTRODUCCIÓN
    # ==========================================
    story.append(PageBookmark('intro'))
    story.append(Paragraph("Introducción", styles['APANivel1']))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "La construcción de soluciones de software robustas, escalables y mantenibles en el tiempo exige que la fase "
        "de Ejecución no comience con una codificación dispersa o empírica, sino con la consolidación rigurosa de una "
        "arquitectura base estandarizada. En el marco del programa de formación tecnológica en Análisis y Desarrollo de "
        "Software del Centro Minero - Regional Boyacá del SENA (2026), la Guía de Aprendizaje G-02 aborda los primeros "
        "pasos técnicos utilizando el framework Django, orientando al aprendiz a transitar desde las especificaciones de diseño "
        "hacia los cimientos operativos de un software web corporativo.",
        styles['APABody']
    ))
    story.append(Paragraph(
        "Django es reconocido a nivel global por su filosofía de 'baterías incluidas' y la adhesión al principio fundamental "
        "DRY (<i>Don't Repeat Yourself</i>). A diferencia de los micro-frameworks como Flask, los cuales demandan el ensamblaje "
        "manual y heterogéneo de componentes de autenticación, ORM y seguridad —lo que incrementa la probabilidad de fallos y "
        "vulnerabilidades en sistemas empresariales—, Django provee una infraestructura integral, madura y probada en producción. "
        "Esta estructura nativa garantiza que las reglas del negocio, el enrutamiento de peticiones, la gestión relacional de datos "
        "y la presentación visual converjan bajo el patrón arquitectónico Modelo-Vista-Template (MVT).",
        styles['APABody']
    ))
    story.append(Paragraph(
        "El presente informe técnico da respuesta exhaustiva y secuencial a las actividades de aprendizaje formuladas en la guía: "
        "la reflexión inicial sobre la modularidad en GAES, la contextualización teórica de los primeros tres capítulos del Manual "
        "Técnico de Desarrollo Web con Django Parte I, la implementación procedimental de la arquitectura en Visual Studio Code "
        "<b>acompañada de capturas de pantalla reales del código fuente programado</b>, la integración de las interfaces frontend "
        "del proyecto formativo 'El Paso Frutería' con su correspondiente catálogo dinámico de productos, y la sustentación del "
        "prototipo funcional evidenciado mediante capturas de ejecución y el control de versiones en GitHub.",
        styles['APABody']
    ))
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 6: CAPÍTULO I - REFLEXIÓN INICIAL
    # ==========================================
    story.append(PageBookmark('cap1'))
    story.append(Paragraph("Capítulo I: Actividades de Reflexión Inicial (Actividad 3.1)", styles['APANivel1']))
    story.append(Spacer(1, 6))

    story.append(PageBookmark('sec1_1'))
    story.append(Paragraph("Importancia de la Modularidad frente a la Estructura Monolítica", styles['APANivel2']))
    story.append(Paragraph(
        "En el marco del trabajo colaborativo en equipos GAES (Grupos Autónomos de Estudio SENA), integrado por los aprendices "
        "<b>Jhon Mario Guamanzar Sierra</b>, <b>Juan Carlos Merchán</b> y <b>Jhon Exander Gutiérrez Moreno</b>, se abordó el primer interrogante "
        "técnico: <i>¿Por qué cree que las empresas de software exigen que el código esté dividido en 'módulos' independientes en "
        "lugar de tener todo en una sola gran carpeta?</i> La respuesta radica en los principios fundamentales de la ingeniería de "
        "software contemporánea: el Principio de Responsabilidad Única (SRP), la Cohesión Alta y el Acoplamiento Débil (<i>Loose Coupling</i>) "
        "(Martin, 2018).",
        styles['APABody']
    ))
    story.append(Paragraph(
        "Cuando un equipo de desarrollo adopta una aproximación monolítica no modular —almacenando todos los modelos, vistas, plantillas "
        "y controladores en una única carpeta o archivo gigante— el proyecto colapsa rápidamente bajo su propia complejidad. Cualquier "
        "modificación menor en la lógica de facturación puede alterar de forma imprevista variables globales que comprometan el módulo "
        "de usuarios. Adicionalmente, el trabajo simultáneo mediante sistemas de control de versiones distribuidos como Git se convierte "
        "en una fuente incesante de conflictos de fusión (<i>merge conflicts</i>), paralizando la productividad del equipo.",
        styles['APABody']
    ))
    story.append(Paragraph(
        "Por el contrario, la arquitectura modular exigida por Django divide el sistema general (el Proyecto) en aplicaciones específicas "
        "(las Apps). Cada aplicación actúa como un módulo autocontenido que administra sus propios modelos de datos (models.py), su lógica "
        "de procesamiento (views.py), sus rutas locales (urls.py), sus validaciones de formulario (forms.py) y sus plantillas de interfaz "
        "(templates/). Esta organización profesional habilita el trabajo colaborativo en paralelo, el mantenimiento focalizado de errores "
        "y la portabilidad de módulos entre diferentes proyectos de software.",
        styles['APABody']
    ))

    story.append(Spacer(1, 6))
    story.append(PageBookmark('sec1_2'))
    story.append(Paragraph("Análisis de Resiliencia y Tolerancia a Fallos del Sistema", styles['APANivel2']))
    story.append(Paragraph(
        "El segundo interrogante planteado en la guía de formación interroga: <i>Si se cae el módulo de 'Inventario', ¿debería caerse todo "
        "el sistema de la empresa?</i> Desde una perspectiva de arquitectura de misión crítica y continuidad del negocio, la respuesta es "
        "un <b>no categórico</b> (Bass et al., 2012).",
        styles['APABody']
    ))
    story.append(Paragraph(
        "En un entorno corporativo real, si el módulo de existencias sufre una interrupción por una consulta de base de datos bloqueada, "
        "un fallo en la capa de persistencia o una actualización fallida, los demás dominios de la empresa —tales como la atención de clientes "
        "en el portal público, la consulta de estados de cuenta o la recepción de tickets de soporte— deben permanecer 100% operativos. "
        "Tener el sistema completamente acoplado en una sola carpeta provoca un efecto dominó (falla en cascada) donde un error tipográfico "
        "en una vista secundaria impide la compilación del intérprete de Python, dejando fuera de servicio la totalidad de la empresa.",
        styles['APABody']
    ))
    story.append(Paragraph(
        "La arquitectura modular de Django implementa el concepto de <i>Aislamiento de Fallos</i> (<i>Fault Isolation</i>). Al segmentar "
        "las rutas mediante la función include() y modularizar las vistas y modelos, las excepciones ocurridas en una app pueden ser "
        "capturadas localmente mediante middleware y manejadores de error HTTP (como errores 500 y 404 controlados), salvaguardando "
        "la estabilidad del resto del ecosistema web corporativo.",
        styles['APABody']
    ))
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 8: CAPÍTULO II - CONTEXTUALIZACIÓN
    # ==========================================
    story.append(PageBookmark('cap2'))
    story.append(Paragraph("Capítulo II: Contextualización y Fundamentos Técnicos (Actividad 3.2)", styles['APANivel1']))
    story.append(Spacer(1, 6))

    story.append(PageBookmark('sec2_1'))
    story.append(Paragraph("Lectura Técnica: Fundamentos de Django y Filosofía de Diseño", styles['APANivel2']))
    story.append(Paragraph(
        "Con base en la lectura analítica de los Capítulos 1, 2 y 3 (hasta la sección 3.9) del <i>Manual Técnico de Desarrollo Web con "
        "Django Parte I</i> (Botello Herrera, 2026), se establecen los orígenes e intenciones de diseño del framework. Creado en 2003 "
        "en la redacción del periódico <i>Lawrence Journal-World</i> para satisfacer los acelerados ciclos de publicación periodística y "
        "liberado como código abierto en 2005 bajo el nombre del virtuoso músico de jazz Django Reinhardt, su diseño responde a dos axiomas: "
        "la no duplicación de código (DRY) y la provisión integral de herramientas esenciales ('baterías incluidas').",
        styles['APABody']
    ))
    story.append(Paragraph(
        "Frente a micro-frameworks minimalistas como Flask, Django provee por defecto un Mapeador Objeto-Relacional (ORM) agnóstico de motor, "
        "un sistema de autenticación seguro contra ataques CSRF, XSS e Inyecciones SQL, y un motor de renderizado de plantillas DTL altamente "
        "optimizado. Esta arquitectura previene la improvisación de componentes de seguridad y garantiza el cumplimiento estricto de las mejores "
        "prácticas internacionales de la industria del software.",
        styles['APABody']
    ))

    story.append(PageBookmark('sec2_2'))
    story.append(Paragraph("Diferenciación Conceptual: Proyecto (La Casa) vs. App (Las Habitaciones)", styles['APANivel2']))
    story.append(Paragraph(
        "Una de las distinciones pedagógicas más relevantes expuestas en el manual radica en la relación jerárquica y funcional "
        "existente entre un <b>Proyecto</b> y una <b>Aplicación (App)</b> en Django. Para comprender este principio, se recurre a la "
        "analogía arquitectónica de una casa residencial:",
        styles['APABody']
    ))
    story.append(Paragraph(
        "• <b>El Proyecto (La Casa):</b> Representa el contenedor general, los cimientos estructurales y las redes de servicios públicos. "
        "En términos técnicos, corresponde al directorio de configuración global (denominado core en nuestra implementación), el cual contiene "
        "el archivo settings.py (parámetros de base de datos, zona horaria, aplicaciones registradas y middleware), el archivo urls.py principal "
        "(el conmutador central de tráfico web) y las interfaces de conexión para servidores de producción (wsgi.py y asgi.py). Un proyecto "
        "no resuelve lógica de negocio puntual; su propósito es coordinar e interconectar a las diferentes apps.",
        styles['APABody']
    ))
    story.append(Paragraph(
        "• <b>Las Apps (Las Habitaciones):</b> Cada habitación tiene una función especializada dentro de la vivienda. La cocina está equipada "
        "exclusivamente para la cocción de alimentos, mientras que la recámara está adaptada para el descanso. Análogamente, en Django una App "
        "es un módulo de software independiente que resuelve un dominio funcional específico del negocio. En nuestro software, la app "
        "inventario se encarga exclusivamente de las existencias, artículos y categorías, manteniendo su propia estructura de datos, pantallas "
        "y direcciones web.",
        styles['APABody']
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 10: PATRÓN MVT Y DIAGRAMA
    # ==========================================
    story.append(PageBookmark('sec2_3'))
    story.append(Paragraph("Patrón de Arquitectura MVT (Modelo - Vista - Template)", styles['APANivel2']))
    story.append(Paragraph(
        "Django implementa una variante especializada del patrón clásico Modelo-Vista-Controlador (MVC), denominada "
        "<b>Modelo-Vista-Template (MVT)</b>. En esta arquitectura, el framework asume de manera automática la responsabilidad "
        "del Controlador tradicional a través del subsistema central de enrutamiento (URL Dispatcher), redefiniendo los tres roles:",
        styles['APABody']
    ))
    story.append(Paragraph(
        "1. <b>Modelo (Model - La Despensa de Datos):</b> Encapsula la lógica de acceso a datos, validación y relaciones relacionales. "
        "Se define mediante clases puras de Python en models.py heredando de models.Model. A través del ORM de Django, las clases y sus "
        "atributos se traducen automáticamente en tablas, columnas y restricciones relacionales en la base de datos subyacente (SQLite en "
        "desarrollo local, PostgreSQL en producción) sin requerir sentencias manuales de lenguaje SQL.",
        styles['APABody']
    ))
    story.append(Paragraph(
        "2. <b>Vista (View - El Chef):</b> Representa el componente de lógica de procesamiento del negocio. En Django, la Vista no es la "
        "pantalla visual que ve el usuario; es la función o clase en Python (views.py) que recibe la petición HTTP (el objeto request), "
        "interroga al Modelo para recuperar o almacenar información y empaqueta dichos datos en un diccionario de Python denominado <i>Contexto</i>.",
        styles['APABody']
    ))
    story.append(Paragraph(
        "3. <b>Plantilla (Template - El Plato Terminado):</b> Constituye la capa de presentación visual. Es un documento HTML estructurado "
        "que integra etiquetas y variables especiales mediante el motor <i>Django Template Language</i> (DTL). La plantilla recibe el contexto "
        "enviado por la Vista mediante la función render(), inyecta dinámicamente los datos y ensambla el código HTML final que se despacha como "
        "Respuesta HTTP (response) hacia el navegador del cliente.",
        styles['APABody']
    ))

    # Figura 1: Diagrama MVT
    story.append(PageBookmark('fig1'))
    story.extend(create_apa_figure(
        "Figura 1",
        "Diagrama de Flujo y Arquitectura del Patrón MVT en Django",
        "diagram_mvt_architecture.png",
        440, 220,
        "Diagrama conceptual estandarizado que modela el ciclo de vida completo de la petición HTTP (Request-Response Lifecycle), "
        "la delegación de rutas mediante include(), la consulta ORM y la inyección de contexto en la plantilla DTL.",
        styles
    ))

    # Tabla 1: MVT vs MVC
    story.append(PageBookmark('tab1'))
    story.extend(create_apa_table(
        "Tabla 1",
        "Matriz Comparativa entre el Patrón MVT y el Patrón MVC Clásico",
        ["Componente", "Patrón MVC Clásico", "Patrón MVT (Django)", "Responsabilidad Principal"],
        [
            ["Modelo (M)", "Model", "Model (models.py)", "Capa de persistencia, reglas de validación y acceso a base de datos."],
            ["Controlador (C / V)", "Controller", "View (views.py)", "Lógica de negocio, orquestación de datos y preparación del contexto."],
            ["Vista / Presentación", "View", "Template (.html / DTL)", "Estructura de interfaz de usuario e inyección dinámica de información."],
            ["Enrutador de Tráfico", "Front Controller", "URL Dispatcher (urls.py)", "Mapeo de rutas URL a funciones ejecutoras de la vista con include()."]
        ],
        [85, 95, 105, 183],
        "Homología técnica funcional entre los paradigmas de arquitectura web MVC tradicional y MVT nativo de Django.",
        styles
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 11: FBV vs CBV Y TABLA 2
    # ==========================================
    story.append(PageBookmark('sec2_4'))
    story.append(Paragraph("Comparativa Técnica: Vistas Basadas en Funciones (FBV) vs. Clases (CBV)", styles['APANivel2']))
    story.append(Paragraph(
        "En la sección 3.8.1 del manual técnico de desarrollo, se analiza una decisión de diseño crucial para la construcción "
        "del módulo de software: la elección entre Vistas Basadas en Funciones (<i>Function-Based Views - FBV</i>) y Vistas Basadas en "
        "Clases (<i>Class-Based Views - CBV</i>).",
        styles['APABody']
    ))

    # Tabla 2: FBV vs CBV
    story.append(PageBookmark('tab2'))
    story.extend(create_apa_table(
        "Tabla 2",
        "Comparativa Técnica: Vistas Basadas en Funciones (FBV) vs. Vistas Basadas en Clases (CBV)",
        ["Criterio", "Vistas Basadas en Funciones (FBV)", "Vistas Basadas en Clases (CBV)"],
        [
            ["Sintaxis de Definición", "def mi_vista(request):", "class MiVista(TemplateView):"],
            ["Paradigma de Programación", "Programación estructurada / funcional estándar de Python.", "Programación Orientada a Objetos (POO), herencia y mixins."],
            ["Curva de Aprendizaje", "Baja e intuitiva; flujo secuencial paso a paso de request y response.", "Media-alta; exige comprender herencia múltiple y métodos del ciclo de vida."],
            ["Ventajas Técnicas", "Máxima legibilidad y flexibilidad para implementar lógicas complejas a medida.", "Reutilización masiva de código (DRY); vistas genéricas listas para operaciones CRUD."],
            ["Riesgos / Desventajas", "Duplicación de código si se construyen múltiples mantenimientos idénticos.", "Dificultad de personalización si la lógica se desvía del comportamiento estándar."],
            ["Decisión en Proyecto", "<b>Adoptada en esta fase inicial</b> para consolidar el ciclo de petición.", "Planificada para la fase de construcción masiva de módulos CRUD."]
        ],
        [90, 189, 189],
        "Criterios de selección arquitectónica para la capa de presentación y control en Django.",
        styles
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 12: DTL SINTAXIS Y FILTROS (TABLAS 3 Y 4)
    # ==========================================
    story.append(PageBookmark('sec2_5'))
    story.append(Paragraph("El Puente de Comunicación: El Diccionario de Contexto y el Motor DTL", styles['APANivel2']))
    story.append(Paragraph(
        "El motor <i>Django Template Language</i> (DTL) establece un protocolo estricto de sintaxis para renderizar variables y evaluar "
        "estructuras de control sin permitir la ejecución arbitraria de código Python dentro del HTML, preservando la seguridad del sistema:",
        styles['APABody']
    ))

    # Tabla 3: Sintaxis DTL
    story.append(PageBookmark('tab3'))
    story.extend(create_apa_table(
        "Tabla 3",
        "Herramientas y Sintaxis Esencial del Django Template Language (DTL)",
        ["Herramienta DTL", "Sintaxis Formal", "Propósito en el Proyecto Formativo"],
        [
            ["Variables Dinámicas", "{{ nombre_variable }}", "Imprime valores simples enviados desde la vista (títulos, nombres, conteos)."],
            ["Etiquetas de Bloque", "{% block contenido %} ... {% endblock %}", "Declara áreas de reemplazo para la herencia dual de plantillas maestras."],
            ["Etiqueta de Extensión", "{% extends 'base_admin.html' %}", "Hereda el cascarón visual común y reutiliza encabezados, sidebars y scripts."],
            ["Ciclos Iterativos", "{% for item in lista %} ... {% endfor %}", "Recorre colecciones de objetos del modelo para construir tablas dinámicas."],
            ["Bifurcaciones Lógicas", "{% if condicion %} ... {% else %} ... {% endif %}", "Evalúa umbrales métricos (ej. advertencias visuales de stock bajo)."],
            ["Comentarios de Plantilla", "{# comentario interno #}", "Anotaciones de ingeniería invisibles en el código fuente del navegador."]
        ],
        [110, 140, 218],
        "Estructuras de marcado del motor DTL implementadas en la solución.",
        styles,
        is_code_col=[1]
    ))

    # Tabla 4: Filtros DTL
    story.append(PageBookmark('tab4'))
    story.extend(create_apa_table(
        "Tabla 4",
        "Filtros DTL más Utilizados en el Proyecto Formativo",
        ["Filtro", "Sintaxis de Ejemplo", "Salida Visual", "Aplicación Práctica en Inventario"],
        [
            ["capfirst", "{{ p.nombre|capfirst }}", "Taladro percutor", "Capitalizar el nombre del artículo comercial."],
            ["upper", "{{ p.categoria.nombre|upper }}", "HERRAMIENTAS", "Uniformar etiquetas de categorías en encabezados."],
            ["floatformat", "{{ p.precio|floatformat:2 }}", "249900.00", "Formatear valores monetarios a dos posiciones decimales."],
            ["date", "{{ p.fecha|date:'d/m/Y' }}", "23/09/2026", "Mostrar marcas temporales en formato local colombiano."],
            ["default", "{{ p.stock|default:'Agotado' }}", "Agotado", "Presentar mensajes de contingencia ante valores nulos."]
        ],
        [70, 130, 98, 170],
        "Filtros de transformación estética aplicados en la capa visual.",
        styles,
        is_code_col=[1]
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 14: CAPÍTULO III - APROPIACIÓN PRÁCTICA Y VENV
    # ==========================================
    story.append(PageBookmark('cap3'))
    story.append(Paragraph("Capítulo III: Apropiación del Conocimiento - Implementación Práctica (Actividad 3.3)", styles['APANivel1']))
    story.append(Spacer(1, 6))

    story.append(PageBookmark('sec3_1'))
    story.append(Paragraph("Aislamiento Profesional: Creación del Entorno Virtual (VENV)", styles['APANivel2']))
    story.append(Paragraph(
        "Siguiendo rigurosamente las fases del manual técnico, se procedió a configurar un entorno de ejecución seguro y aislado. "
        "En la consola PowerShell de Visual Studio Code se ejecutó la instrucción de generación del entorno: "
        "<code>python -m venv .venv</code>. Seguidamente, se activó la política de ejecución local mediante el script "
        "<code>.\\.venv\\Scripts\\Activate.ps1</code>, garantizando que todas las dependencias y bibliotecas de terceros residan "
        "exclusivamente en el alcance del proyecto sin colisionar con el intérprete global del sistema operativo.",
        styles['APABody']
    ))
    story.append(Paragraph(
        "Posteriormente, con el entorno virtual debidamente activado (verificado mediante el prefijo <code>(.venv)</code> en la terminal), "
        "se instalaron las dependencias del proyecto mediante <code>.\\.venv\\Scripts\\pip install -r requirements.txt</code>, "
        "garantizando la disponibilidad de Django 6.1.1, ReportLab 5.0.1 y PyMuPDF 1.28.2.",
        styles['APABody']
    ))

    story.append(PageBookmark('sec3_2'))
    story.append(Paragraph("Inicialización del Proyecto Django con Arquitectura Limpia", styles['APANivel2']))
    story.append(Paragraph(
        "Para preservar una jerarquía de archivos limpia y evitar la generación de subcarpetas redundantes que suelen ocurrir en "
        "proyectos principiantes (ej. <i>mi_proyecto/mi_proyecto/</i>), se inicializó el framework ejecutando la instrucción con punto terminal:",
        styles['APABody']
    ))
    story.append(Paragraph("<code>django-admin startproject core .</code>", styles['APACodeBlock']))
    story.append(Paragraph(
        "Esta convención le indica a Django que ubique el conmutador de comandos <code>manage.py</code> en el directorio raíz de la solución "
        "y agrupe los archivos de configuración arquitectónica en una carpeta central denominada <code>core</code>.",
        styles['APABody']
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 15: CÓDIGO REAL SETTINGS.PY (FIGURA 2)
    # ==========================================
    story.append(PageBookmark('sec3_3'))
    story.append(Paragraph("Configuración Regional y Directorios Globales en settings.py", styles['APANivel2']))
    story.append(Paragraph(
        "Con el fin de adaptar el sistema a la normativa y contexto geográfico de Colombia, se modificaron los parámetros de "
        "internacionalización en el archivo <code>core/settings.py</code> estableciendo el idioma en español colombiano (<code>es-co</code>) "
        "y la zona horaria en <code>America/Bogota</code>. Asimismo, se registraron las aplicaciones del proyecto en <code>INSTALLED_APPS</code> "
        "y se definieron las rutas globales para plantillas maestras y recursos estáticos mediante la variable de sistema <code>BASE_DIR</code>.",
        styles['APABody']
    ))

    # Figura 2: Código Real settings.py
    story.append(PageBookmark('fig2'))
    story.extend(create_apa_figure(
        "Figura 2",
        "Código Fuente Real: Configuración Regional y Módulos en core/settings.py",
        "screenshot_code_settings.png",
        440, 245,
        "Captura de pantalla real del código fuente de core/settings.py programado en el proyecto, donde se aprecia el registro de la app "
        "'inventario', la ruta global de plantillas duales (BASE_DIR / 'templates'), la configuración regional colombiana y los directorios estáticos.",
        styles
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 16: CREACIÓN DE APP Y NAMESPACING
    # ==========================================
    story.append(PageBookmark('sec3_4'))
    story.append(Paragraph("Creación y Registro de la Primera Aplicación Modular (inventario)", styles['APANivel2']))
    story.append(Paragraph(
        "Para materializar el principio de modularidad, se creó el módulo funcional de existencias mediante el comando: "
        "<code>python manage.py startapp inventario</code>. Acto seguido, se ejecutó el paso crítico obligatorio de registrar "
        "la nueva aplicación en la lista <code>INSTALLED_APPS</code> del archivo <code>core/settings.py</code>.",
        styles['APABody']
    ))

    story.append(PageBookmark('sec3_5'))
    story.append(Paragraph("Estructura Interna del Módulo y Namespacing de Plantillas", styles['APANivel2']))
    story.append(Paragraph(
        "Siguiendo las pautas de ingeniería de la sección 3.4 del manual, se completó la anatomía interna de la aplicación "
        "creando manualmente los archivos <code>urls.py</code>, <code>forms.py</code> y la carpeta de plantillas especializada. "
        "Para resolver el fenómeno de <i>Colisión de Nombres</i> —en el cual Django reúne todas las plantillas de todas las apps "
        "en una sola bolsa virtual compartida y podría confundir archivos homónimos como <i>index.html</i>— se implementó la técnica "
        "estándar de <b>Namespacing</b>, anidando una subcarpeta con el nombre del módulo: "
        "<code>inventario/templates/inventario/index.html</code> y subcarpetas para las entidades: "
        "<code>inventario/templates/inventario/productos/lista.html</code>.",
        styles['APABody']
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 17: CÓDIGO REAL ENRUTAMIENTO (FIGURA 3)
    # ==========================================
    story.append(PageBookmark('sec3_6'))
    story.append(Paragraph("Enrutamiento Desacoplado mediante include() en core/urls.py", styles['APANivel2']))
    story.append(Paragraph(
        "Para lograr un desacoplamiento limpio, las rutas no se concentraron en un único archivo global. El proyecto principal "
        "delega el tráfico web hacia el módulo mediante la función <code>include()</code> en <code>core/urls.py</code>, integrando a su "
        "vez los endpoints canónicos de la tienda y catálogo de frutas ('El Paso Frutería'). En <code>inventario/urls.py</code> se definió "
        "el espacio de nombres local (<code>app_name = 'inventario'</code>) para garantizar la navegación modular.",
        styles['APABody']
    ))

    # Figura 3: Código Real URLs
    story.append(PageBookmark('fig3'))
    story.extend(create_apa_figure(
        "Figura 3",
        "Código Fuente Real: Enrutamiento Modular Desacoplado con include()",
        "screenshot_code_urls.png",
        440, 220,
        "Captura de pantalla real del código fuente de core/urls.py e inventario/urls.py, evidenciando el mecanismo de delegación "
        "mediante la función include(), las rutas integradas de la tienda y catálogo de frutas ('El Paso Frutería') y el uso del espacio de nombres (app_name = 'inventario').",
        styles
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 18: CÓDIGO REAL VISTAS (FIGURA 4)
    # ==========================================
    story.append(PageBookmark('sec3_7'))
    story.append(Paragraph("Lógica del Controlador y Diccionario de Contexto en views.py", styles['APANivel2']))
    story.append(Paragraph(
        "En la capa de lógica, se estructuraron controladores desacoplados: en <code>core/views.py</code> se procesan las vistas públicas "
        "de la tienda y catálogo de frutas (<code>tienda_fruteria</code> y <code>catalogo_frutas</code>), mientras que en <code>inventario/views.py</code> "
        "la función <code>dashboard_inventario</code> ejecuta consultas agregadas al ORM y despacha el diccionario de contexto al motor DTL.",
        styles['APABody']
    ))

    # Figura 4: Código Real Views
    story.append(PageBookmark('fig4'))
    story.extend(create_apa_figure(
        "Figura 4",
        "Código Fuente Real: Vista Controladora e Inyección de Contexto en views.py",
        "screenshot_code_views.png",
        440, 225,
        "Captura de pantalla real de las vistas en core/views.py e inventario/views.py, evidenciando las funciones controladoras de El Paso Frutería "
        "y el cálculo de existencias dinámicas en el dashboard despachadas mediante render().",
        styles
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 19: CÓDIGO REAL MODELOS (FIGURA 5)
    # ==========================================
    story.append(PageBookmark('sec3_8'))
    story.append(Paragraph("Modelado de Datos Relacional y Persistencia con el ORM", styles['APANivel2']))
    story.append(Paragraph(
        "En la capa de persistencia (<code>inventario/models.py</code>), se codificaron las entidades relacionales <code>Categoria</code> y "
        "<code>Producto</code> con clave foránea asociativa (<code>ForeignKey</code>) y métodos de representación legible (<code>__str__</code>):",
        styles['APABody']
    ))

    # Figura 5: Código Real Models
    story.append(PageBookmark('fig5'))
    story.extend(create_apa_figure(
        "Figura 5",
        "Código Fuente Real: Modelos Relacionales y Persistencia ORM en models.py",
        "screenshot_code_models.png",
        440, 230,
        "Captura de pantalla real del archivo inventario/models.py que define los modelos relacionales Categoria y Producto con tipos de datos "
        "estrictos, llave foránea asociativa (models.CASCADE) y métodos de representación formal __str__().",
        styles
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 20: CÓDIGO REAL PLANTILLAS (FIGURA 6)
    # ==========================================
    story.append(PageBookmark('sec3_9'))
    story.append(Paragraph("Arquitectura Visual con Herencia Dual de Plantillas y Bootstrap 5", styles['APANivel2']))
    story.append(Paragraph(
        "Considerando que los usuarios de un software empresarial poseen roles claramente diferenciados, se construyó un "
        "sistema de <b>Herencia Dual</b> integrando Bootstrap 5 vía CDN: la plantilla <code>base_cliente.html</code> para la interfaz "
        "pública y <code>base_admin.html</code> con barra lateral (*Sidebar*) para el módulo de gestión.",
        styles['APABody']
    ))

    # Figura 6: Código Real Plantillas DTL
    story.append(PageBookmark('fig6'))
    story.extend(create_apa_figure(
        "Figura 6",
        "Código Fuente Real: Plantilla DTL con Herencia Dual en index.html",
        "screenshot_code_templates.png",
        440, 225,
        "Captura de pantalla real de la plantilla templates/home.html evidenciando la herencia mediante {% extends 'base_cliente.html' %}, "
        "la inyección de metadatos institucionales y los botones canónicos de navegación directa hacia la tienda y catálogo de frutas.",
        styles
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 21: CAPÍTULO IV - TRANSFERENCIA Y TERMINAL (FIGURA 7)
    # ==========================================
    story.append(PageBookmark('cap4'))
    story.append(Paragraph("Capítulo IV: Transferencia del Conocimiento - Prototipo y Evidencias (Actividad 3.4)", styles['APANivel1']))
    story.append(Spacer(1, 6))

    story.append(PageBookmark('sec4_1'))
    story.append(Paragraph("Puesta en Marcha y Verificación del Servidor Local", styles['APANivel2']))
    story.append(Paragraph(
        "La comprobación integral de la arquitectura se realizó levantando el servidor de desarrollo mediante el comando "
        "<code>python manage.py runserver 127.0.0.1:8000</code>. El subsistema <i>StatReloader</i> verificó la sintaxis del código "
        "y confirmó: <i>'System check identified no issues (0 silenced)'</i>, atendiendo las peticiones con código de estado 200 OK.",
        styles['APABody']
    ))

    # Figura 7: Terminal
    story.append(PageBookmark('fig7'))
    story.extend(create_apa_figure(
        "Figura 7",
        "Consola Terminal con Entorno Virtual (.venv) y Servidor Django Activo",
        "screenshot_terminal_runserver.png",
        440, 205,
        "Captura de la consola PowerShell que certifica la activación del entorno virtual .venv, la verificación del sistema sin "
        "advertencias y la atención de solicitudes HTTP 200 OK para las rutas pública (/), comercial (/tienda/), catálogo (/catalogo-frutas/) y administrativa (/inventario/).",
        styles
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 22: INTERFAZ PÚBLICA (FIGURA 8)
    # ==========================================
    story.append(PageBookmark('sec4_2'))
    story.append(Paragraph("Evidencias Gráficas de Navegación Pública y Administrativa", styles['APANivel2']))
    story.append(Paragraph(
        "A continuación, se documentan las evidencias gráficas directas del prototipo funcional ejecutándose en el servidor local "
        "con sus respectivas pruebas de enrutamiento y herencia dual.",
        styles['APABody']
    ))

    # Figura 8: Portal Público
    story.append(PageBookmark('fig8'))
    story.extend(create_apa_figure(
        "Figura 8",
        "Interfaz Pública de Usuario basada en base_cliente.html y Bootstrap 5",
        "screenshot_public_home.png",
        440, 230,
        "Vista de la página de inicio (Landing Page) en http://127.0.0.1:8000/, donde se aprecia la barra de navegación pública, "
        "el banner corporativo con estilos responsivos de Bootstrap 5 y la tarjeta descriptiva de los módulos de software.",
        styles
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 23: INTEGRACIÓN PROYECTO FORMATIVO "EL PASO FRUTERÍA" (FIGURA 9)
    # ==========================================
    story.append(PageBookmark('sec4_3'))
    story.append(Paragraph("Integración del Proyecto Formativo: Tienda Virtual y Catálogo de Frutas ('El Paso Frutería')", styles['APANivel2']))
    story.append(Paragraph(
        "En consonancia con los objetivos del proyecto formativo institucional y los recursos frontend desarrollados "
        "(archivos HTML modulares, hojas de estilos CSS personalizadas y lógica de interacción en JavaScript), "
        "se realizó la integración técnica de la tienda comercial y del catálogo frutícola interactivo al ecosistema Django. "
        "Para lograr un acoplamiento limpio sin alterar la modularidad, se ubicaron los recursos en <code>static/css/</code> "
        "(incluyendo <code>opcion4.css</code> y <code>frutas.css</code>) y <code>static/js/</code> (<code>carrusel.js</code> y "
        "<code>catalogo.js</code>). Las plantillas fueron organizadas en <code>templates/fruteria/tienda.html</code> y "
        "<code>templates/fruteria/catalogo_frutas.html</code>, cargando los recursos estáticos mediante la etiqueta DTL "
        "<code>{% load static %}</code> y enlazando dinámicamente las rutas canónicas <code>/tienda/</code> y "
        "<code>/catalogo-frutas/</code> definidas en <code>core/urls.py</code>.",
        styles['APABody']
    ))

    # Figura 9: Tienda Frutería
    story.append(PageBookmark('fig9'))
    story.extend(create_apa_figure(
        "Figura 9",
        "Interfaz Comercial de la Tienda de Frutas ('El Paso Frutería') en /tienda/",
        "screenshot_tienda_fruteria.png",
        440, 250,
        "Captura en alta resolución de la tienda comercial 'El Paso Frutería' en http://127.0.0.1:8000/tienda/, visualizando "
        "el carrusel de promociones, tarjetas de productos destacados, navegación interactiva y diseño visual moderno "
        "integrado bajo la arquitectura de plantillas y archivos estáticos de Django.",
        styles
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 24: CATÁLOGO INTERACTIVO DE FRUTAS (FIGURA 10)
    # ==========================================
    story.append(PageBookmark('sec4_4'))
    story.append(Paragraph("Catálogo Interactivo y Filtrado Dinámico de Productos Frutícolas", styles['APANivel2']))
    story.append(Paragraph(
        "Para ofrecer una experiencia de usuario (UX) óptima, el catálogo accesible en <code>/catalogo-frutas/</code> "
        "organiza la oferta comercial en categorías especializadas (Cítricas, Tropicales, Frutos Rojos / Berries y Exóticas). "
        "La interfaz incorpora filtrado reactivo en el lado del cliente y vinculación directa hacia el sistema de inventario, "
        "permitiendo a los clientes explorar las existencias, consultar precios unitarios y visualizar la información nutricional.",
        styles['APABody']
    ))

    # Figura 10: Catálogo Interactivo
    story.append(PageBookmark('fig10'))
    story.extend(create_apa_figure(
        "Figura 10",
        "Catálogo Interactivo y Filtrado de Frutas por Categoría en /catalogo-frutas/",
        "screenshot_catalogo_frutas.png",
        440, 260,
        "Pantalla del catálogo interactivo en http://127.0.0.1:8000/catalogo-frutas/, exhibiendo la grilla responsiva de frutas, "
        "los selectores de categoría activos, los precios comerciales y la vinculación conceptual con el inventario del sistema.",
        styles
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 25: GESTIÓN ADMINISTRATIVA DEL INVENTARIO (FIGURAS 11 Y 12)
    # ==========================================
    story.append(PageBookmark('sec4_5'))
    story.append(Paragraph("Gestión Administrativa del Inventario de Productos Frutícolas", styles['APANivel2']))
    story.append(Paragraph(
        "La capa administrativa del módulo <code>inventario</code> se alimentó con las categorías y existencias reales del dominio "
        "comercial de frutas (Naranjas Valencia, Limón Tahití, Mangos, Piñas, Berries y Pitahayas). El panel central "
        "(<code>/inventario/</code>) calcula métricas en tiempo real mediante el ORM (conteo total de existencias y alertas de "
        "bajo stock para reabastecimiento), articulando la operación de trastienda con la tienda de cara al público.",
        styles['APABody']
    ))

    # Figura 11: Dashboard Inventario
    story.append(PageBookmark('fig11'))
    story.extend(create_apa_figure(
        "Figura 11",
        "Dashboard Administrativo del Módulo de Inventario con Stock Frutícola",
        "screenshot_admin_dashboard.png",
        440, 200,
        "Pantalla del panel administrativo en http://127.0.0.1:8000/inventario/, exhibiendo el menú lateral (Sidebar), "
        "tarjetas métricas con contadores dinámicos alimentados desde el ORM y tabla interactiva de existencias de frutas.",
        styles
    ))

    # Figura 12: Catálogo de Productos Administrativo
    story.append(PageBookmark('fig12'))
    story.extend(create_apa_figure(
        "Figura 12",
        "Catálogo de Existencias con Namespacing de Plantillas en Django",
        "screenshot_admin_catalog.png",
        440, 190,
        "Pantalla del catálogo en http://127.0.0.1:8000/inventario/productos/, evidenciando la resolución correcta de plantillas "
        "namespaced (inventario/productos/lista.html) heredadas de base_admin.html.",
        styles
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 26: PANEL ADMIN DJANGO Y REPO GITHUB (FIGURA 13)
    # ==========================================
    # Figura 13: Panel de Administración Nativo
    story.append(PageBookmark('fig13'))
    story.extend(create_apa_figure(
        "Figura 13",
        "Panel Administrativo Nativo de Django con Modelos Registrados",
        "screenshot_django_admin_auth.png",
        440, 195,
        "Interfaz del panel nativo de administración en http://127.0.0.1:8000/admin/ autenticada con el superusuario del sistema, "
        "demostrando la administración directa de los modelos Categoria y Producto con estilos CSS oficiales completos.",
        styles
    ))

    story.append(PageBookmark('sec4_6'))
    story.append(Paragraph("Repositorio Oficial en GitHub y Control de Versiones Git", styles['APANivel2']))
    story.append(Paragraph(
        "Para garantizar la transparencia, reproducibilidad y trazabilidad técnica del desarrollo, el código fuente completo del "
        "proyecto formativo fue versionado mediante Git y alojado en el repositorio oficial de GitHub asignado:",
        styles['APABody']
    ))
    story.append(Paragraph(
        "• <b>URL Oficial del Repositorio:</b> <font color='#0d6efd'><u>https://github.com/jhonmariog102015-a11y/jira_actividad-grupal.git</u></font><br/>"
        "• <b>Rama Principal de Despliegue:</b> <code>main</code><br/>"
        "• <b>Equipo Desarrollador (GAES):</b> Jhon Mario Guamanzar Sierra (Cuenta GitHub: <code>jhonmariog102015-a11y</code>), Juan Carlos Merchán, Jhon Exander Gutiérrez Moreno",
        styles['APABodyNoIndent']
    ))
    story.append(Paragraph(
        "Instrucciones técnicas para la réplica del prototipo en cualquier equipo de cómputo:",
        styles['APABody']
    ))
    story.append(Paragraph(
        "<code>git clone https://github.com/jhonmariog102015-a11y/jira_actividad-grupal.git<br/>"
        "cd jira_actividad-grupal<br/>"
        "python -m venv .venv<br/>"
        ".\\.venv\\Scripts\\Activate.ps1<br/>"
        "pip install -r requirements.txt<br/>"
        "python manage.py migrate<br/>"
        "python manage.py runserver</code>",
        styles['APACodeBlock']
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 27: MATRIZ DE CRITERIOS Y CONCLUSIONES
    # ==========================================
    story.append(PageBookmark('sec4_7'))
    story.append(Paragraph("Criterios de Evaluación y Lista de Chequeo de la Guía G-02", styles['APANivel2']))
    story.append(Paragraph(
        "En la Tabla 5 se sintetizan los criterios e instrumentos de evaluación establecidos formalmente por el SENA en la Guía G-02, "
        "así como su nivel de cumplimiento dentro de este informe técnico y prototipo.",
        styles['APABody']
    ))

    # Tabla 5: Matriz de Evaluación
    story.append(PageBookmark('tab5'))
    story.extend(create_apa_table(
        "Tabla 5",
        "Matriz de Criterios de Evaluación de la Guía de Aprendizaje G-02",
        ["Ítem de Evaluación", "Requerimiento Guía G-02", "Evidencia de Cumplimiento", "Estado"],
        [
            ["Aislamiento de Entorno", "Creación de entorno virtual VENV para gestión segura de librerías.", "Entorno .venv configurado, activado y documentado en requirements.txt.", "Aprobado (100%)"],
            ["Modularidad", "Estructuración de Apps independientes desacopladas de la raíz.", "Módulo 'inventario' creado con urls.py, forms.py, models.py y views.py.", "Aprobado (100%)"],
            ["Enrutamiento", "Configuración de rutas con include() para interfaces públicas y privadas.", "core/urls.py delegando a inventario/urls.py y rutas canónicas a /tienda/ y /catalogo-frutas/.", "Aprobado (100%)"],
            ["Arquitectura Visual", "Motor de plantillas DTL y Bootstrap 5 con Herencia Dual.", "base_cliente.html, base_admin.html y plantillas de frutería integradas.", "Aprobado (100%)"],
            ["Evidencias y Sustentación", "Repositorio GitHub y capturas reales de código y ejecución en informe APA 7.", "Informe técnico completo en PDF con 13 figuras y repositorio en GitHub.", "Aprobado (100%)"]
        ],
        [85, 125, 185, 73],
        "Verificación formal de cumplimiento de la Lista de Chequeo según formato GFPI-F-135 V04 del SENA.",
        styles
    ))

    story.append(Spacer(1, 10))
    story.append(PageBookmark('conclusiones'))
    story.append(Paragraph("Conclusiones", styles['APANivel1']))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "1. La implementación de la arquitectura base en Django confirmó que la adopción temprana del patrón MVT y la modularidad de "
        "aplicaciones permite organizar proyectos empresariales complejos, garantizando que el mantenimiento futuro y la adición de nuevas "
        "funcionalidades no comprometan la estabilidad del núcleo del sistema.",
        styles['APABody']
    ))
    story.append(Paragraph(
        "2. El sistema de Herencia Dual (base_cliente.html y base_admin.html) en conjunto con Bootstrap 5 y hojas de estilos especializadas "
        "demostró ser una solución altamente eficiente para resolver las exigencias visuales de múltiples perfiles de usuario, evitando "
        "la duplicidad de marcado HTML y facilitando una navegación intuitiva y responsiva.",
        styles['APABody']
    ))
    story.append(Paragraph(
        "3. La técnica de Namespacing en plantillas y el enrutamiento desacoplado mediante la función include() resuelven de raíz las "
        "colisiones de nombres en proyectos colaborativos, habilitando el desarrollo paralelo en equipos de trabajo mediante control de versiones.",
        styles['APABody']
    ))
    story.append(Paragraph(
        "4. La articulación práctica de las interfaces frontend del proyecto formativo ('El Paso Frutería') con el backend Django validó la "
        "flexibilidad del motor DTL y del subsistema de archivos estáticos (Static Files), permitiendo la transición fluida desde maquetas "
        "independientes hacia una aplicación web unificada, dinámica y lista para su evolución hacia transacciones de comercio electrónico.",
        styles['APABody']
    ))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 26: REFERENCIAS BIBLIOGRÁFICAS
    # ==========================================
    story.append(PageBookmark('referencias'))
    story.append(Paragraph("Referencias Bibliográficas", styles['APANivel1']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Aguilar Joyanes, L. (2008). <i>Fundamentos de programación: Algoritmos, estructura de datos y objetos</i> (4.ª ed.). McGraw-Hill Interamericana.",
        styles['APAReferencia']
    ))
    story.append(Paragraph(
        "Bass, L., Clements, P., & Kazman, R. (2012). <i>Software architecture in practice</i> (3rd ed.). Addison-Wesley Professional.",
        styles['APAReferencia']
    ))
    story.append(Paragraph(
        "Botello Herrera, A. R. (2026). <i>Manual técnico de desarrollo web con Django: Fundamentos de arquitectura, ORM y patrón MVT (Parte I)</i>. Servicio Nacional de Aprendizaje [SENA].",
        styles['APAReferencia']
    ))
    story.append(Paragraph(
        "Django Software Foundation. (2026a). <i>Django documentation: Design philosophies</i>. Django Project. https://docs.djangoproject.com/en/6.0/misc/design-philosophies/",
        styles['APAReferencia']
    ))
    story.append(Paragraph(
        "Django Software Foundation. (2026b). <i>The Django template language</i>. Django Project. https://docs.djangoproject.com/en/6.0/topics/templates/",
        styles['APAReferencia']
    ))
    story.append(Paragraph(
        "Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). <i>Design patterns: Elements of reusable object-oriented software</i>. Addison-Wesley.",
        styles['APAReferencia']
    ))
    story.append(Paragraph(
        "Martin, R. C. (2018). <i>Clean architecture: A craftsman's guide to software structure and design</i>. Prentice Hall.",
        styles['APAReferencia']
    ))
    story.append(Paragraph(
        "Servicio Nacional de Aprendizaje. (2026). <i>Guía de aprendizaje G-02: Arquitectura base, enrutamiento y plantillas (Código 220501096-01)</i>. SENA Centro Minero - Regional Boyacá.",
        styles['APAReferencia']
    ))

    return story


def build_complete_pdf(output_filename):
    styles = get_apa_styles()

    # PASADA 1: Determinar el número exacto de páginas donde cae cada marcador
    print("Iniciando Pasada 1 para indexación de páginas...")
    temp_filename = "temp_pass1.pdf"
    doc_pass1 = SimpleDocTemplate(
        temp_filename,
        pagesize=letter,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    story_pass1 = generate_pdf_story(styles)
    doc_pass1.build(story_pass1, canvasmaker=APANumberedCanvas)
    print("Registro de páginas obtenido:", PAGE_REGISTRY)

    # PASADA 2: Generar el documento final definitivo con la Tabla de Contenido precisa
    print("Iniciando Pasada 2 para compilación definitiva con Normas APA 7ma edición...")
    doc_final = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    story_final = generate_pdf_story(styles)
    doc_final.build(story_final, canvasmaker=APANumberedCanvas)

    if os.path.exists(temp_filename):
        try:
            os.remove(temp_filename)
        except Exception:
            pass

    print(f"Documento generado exitosamente en: {output_filename}")


if __name__ == '__main__':
    out_pdf = os.path.join(os.getcwd(), 'Informe_Tecnico_Arquitectura_Base_Django_APA7.pdf')
    build_complete_pdf(out_pdf)
