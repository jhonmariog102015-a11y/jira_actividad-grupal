# Arquitectura Base, Enrutamiento y Plantillas en Django
## Solución Técnica y Metodológica - Guía de Aprendizaje G-02

**Servicio Nacional de Aprendizaje (SENA)**  
**Centro Minero - Regional Boyacá**  
**Programa:** Análisis y Desarrollo de Software (ADSO) | **Ficha de Caracterización:** 3321349  
**Proyecto Formativo:** Desarrollo de Aplicativos Web para Control y Gestión de la Información  
**Fase:** Ejecución | **Competencia:** 220501096 - Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo  
**Equipo de Desarrollo (GAES):**  
- Jhon Mario Guamanzar Sierra  
- Juan Carlos Merchán  
- Jhon Exander Gutiérrez Moreno  
**Instructor Técnico:** Ing. Antony Reynel Botello Herrera  
**Fecha:** Septiembre de 2026  

---

## 📌 Descripción del Proyecto

Este repositorio contiene la arquitectura base, configuración de enrutamiento modular y sistema dual de plantillas navegables desarrollado con el framework **Django 6.0** y **Bootstrap 5**, en estricto cumplimiento de los lineamientos del **Manual Técnico de Desarrollo Web con Django Parte I (Capítulos 1 al 3.9)** y la **Guía G-02**, integrando además las interfaces visuales del proyecto formativo institucional **"El Paso Frutería"** (tienda comercial y catálogo dinámico con filtrado interactivo).

Se incluye como entregable principal el documento técnico formal en formato PDF:
📄 **`Informe_Tecnico_Arquitectura_Base_Django_APA7.pdf`**  
*(26 páginas estructuradas bajo Normas APA 7.ª edición con portada estudiantil, tabla de contenido dinámica, lista de tablas y 13 figuras, análisis del debate GAES, mapas conceptuales MVT, código fuente real capturado, capturas de navegación del prototipo y referencias bibliográficas).*

---

## 🏗️ Arquitectura de Software Implementada

El proyecto implementa el patrón arquitectónico **Modelo-Vista-Template (MVT)** con modularidad desacoplada:

1. **Aislamiento Profesional (VENV):** Gestión segura de dependencias mediante entorno virtual `.venv`.
2. **Modularidad (Proyecto vs. Apps):**
   - **`core/` (La Casa):** Contenedor principal de configuración (`settings.py`), enrutador maestro (`urls.py`) y servidor WSGI/ASGI.
   - **`inventario/` (La Habitación):** Módulo funcional de existencias con sus propios modelos (`models.py`), vistas (`views.py`), rutas delegadas (`urls.py`), formularios (`forms.py`) y plantillas especializadas.
3. **Namespacing de Plantillas:** Organización en subcarpetas (`inventario/templates/inventario/...`) para prevenir la colisión de nombres en la bolsa virtual de Django.
4. **Herencia Dual con Bootstrap 5:**
   - **`base_cliente.html`:** Plantilla maestra para la interfaz pública (clientes y visitantes).
   - **`base_admin.html`:** Plantilla maestra tipo Dashboard con menú lateral (*Sidebar*) para la administración interna.
5. **Configuración Regional:** Parametrización en `core/settings.py` para Colombia (`LANGUAGE_CODE = 'es-co'`, `TIME_ZONE = 'America/Bogota'`).
6. **Persistencia ORM:** Modelos relacionales `Categoria` y `Producto` conectados a base de datos SQLite con claves foráneas y administración nativa.

---

## 📂 Estructura de Directorios

```text
jira_actividad-grupal/
├── core/                                # Configuración global del proyecto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                      # Configuración regional (es-co), apps y static/templates
│   ├── urls.py                          # Enrutador principal con delegación include()
│   ├── views.py                         # Vista pública (Landing Page)
│   └── wsgi.py
├── inventario/                          # Módulo funcional de Inventario (App)
│   ├── migrations/                      # Migraciones del ORM
│   ├── templates/                       # Plantillas con Namespacing
│   │   └── inventario/
│   │       ├── productos/
│   │       │   └── lista.html           # Catálogo detallado de productos
│   │       ├── stock/                   # Subcarpeta de entidad stock
│   │       └── index.html               # Dashboard administrativo de inventario
│   ├── admin.py                         # Registro de Categoria y Producto en panel de administración
│   ├── apps.py                          # Configuración de la App
│   ├── forms.py                         # Formularios validados de productos
│   ├── models.py                        # Modelos ORM relacionales (Categoria y Producto)
│   ├── urls.py                          # Enrutador local con app_name = 'inventario'
│   └── views.py                         # Vistas FBV con inyección de contexto dinámico
├── static/                              # Recursos estáticos globales
│   ├── css/custom.css                   # Hoja de estilos complementaria
│   └── js/main.js                       # Scripts de frontend
├── templates/                           # Plantillas maestras globales (Herencia Dual)
│   ├── partials/                        # Fragmentos reutilizables
│   ├── base_admin.html                  # Cascarón administrativo con Sidebar y Bootstrap 5
│   ├── base_cliente.html                # Cascarón público con Navbar y Bootstrap 5
│   └── home.html                        # Página de inicio pública
├── .gitignore                           # Exclusión de venv, cache y temporales
├── build_apa_pdf.py                     # Script generador del informe técnico APA 7 en PDF
├── create_figures.py                    # Generador de capturas y diagramas de arquitectura
├── db.sqlite3                           # Base de datos local con datos de prueba
├── manage.py                            # Gestor de comandos de Django
├── requirements.txt                     # Lista de dependencias del proyecto
├── Informe_Tecnico_Arquitectura_Base_Django_APA7.pdf   # Entregable formal APA 7 (23 págs)
└── README.md                            # Documentación técnica del repositorio
```

---

## 🚀 Guía de Instalación y Ejecución Local

Para clonar y poner en marcha este prototipo funcional en su servidor local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/jhonmariog102015-a11y/jira_actividad-grupal.git
cd jira_actividad-grupal
```

### 2. Crear y activar el Entorno Virtual (VENV)
**En Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**En Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Aplicar Migraciones de Base de Datos
```bash
python manage.py migrate
```

### 5. Levantar el Servidor de Desarrollo
```bash
python manage.py runserver
```

---

## 🌐 Endpoints y Rutas del Prototipo

Una vez iniciado el servidor, abra su navegador web en las siguientes direcciones:

| Ruta URL | Tipo de Interfaz | Plantilla Base Utilizada | Descripción |
| :--- | :--- | :--- | :--- |
| `http://127.0.0.1:8000/` | Pública (General) | `base_cliente.html` | Página de bienvenida (Landing Page) con Bootstrap 5 |
| `http://127.0.0.1:8000/tienda/` | Pública (Comercial) | `templates/fruteria/tienda.html` | Tienda virtual "El Paso Frutería" con carrusel y ofertas |
| `http://127.0.0.1:8000/catalogo-frutas/` | Pública (Catálogo) | `templates/fruteria/catalogo_frutas.html` | Catálogo interactivo con filtrado de frutas por categorías |
| `http://127.0.0.1:8000/inventario/` | Privada (Administración) | `base_admin.html` | Dashboard con tarjetas métricas y tabla de stock de frutas |
| `http://127.0.0.1:8000/inventario/productos/` | Privada (Catálogo Admin) | `base_admin.html` | Catálogo de existencias namespaced |
| `http://127.0.0.1:8000/admin/` | Panel Django | Nativa Django (es-co) | Panel de administración con login y modelos |

*Credenciales de superusuario para el panel `/admin/`:*  
- **Usuario:** `admin`  
- **Contraseña:** `admin123`  

---

## 📊 Matriz de Cumplimiento de la Guía G-02

| Actividad de Aprendizaje | Criterio Requerido | Implementación y Evidencia | Estado |
| :--- | :--- | :--- | :---: |
| **3.1 Reflexión Inicial** | Debate en GAES sobre modularidad vs. monolito y tolerancia a fallos. | Capítulo I del informe técnico PDF con análisis de acoplamiento débil y resiliencia. | ✅ 100% |
| **3.2 Contextualización** | Diferencia Proyecto vs. App y Patrón de Arquitectura MVT. | Capítulo II del informe técnico PDF con diagrama de flujo, tablas comparativas y DTL. | ✅ 100% |
| **3.3 Apropiación** | VENV, settings.py regional, app modular y herencia dual con Bootstrap 5. | Capítulo III del informe técnico PDF, código fuente documentado y repositorio Git. | ✅ 100% |
| **3.4 Transferencia** | Servidor local navegable, prototipo funcional y evidencias con capturas. | Capítulo IV del informe técnico PDF con 13 figuras formales y ejecución 200 OK. | ✅ 100% |

---

## 📄 Documento Entregable en Normas APA 7.ª Edición

Consulte el documento completo adjunto en la raíz de este repositorio:  
👉 **[`Informe_Tecnico_Arquitectura_Base_Django_APA7.pdf`](./Informe_Tecnico_Arquitectura_Base_Django_APA7.pdf)**
