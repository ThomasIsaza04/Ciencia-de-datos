# Unidad de Correspondencia SENA - API RESTful

API RESTful desarrollada con **FastAPI** y **SQLite3** nativo para la gestión modular e integral del flujo de correspondencia institucional (Remitentes y Radicados) en el SENA.

---

## Arquitectura del Proyecto

El proyecto está estructurado bajo una arquitectura limpia en capas, separando responsabilidades en módulos independientes:

```text
.
├── correspondencia_sena.db      # Base de datos SQLite3
├── requirements.txt            # Dependencias del proyecto
└── scripts/
    └── correspondencia/
        ├── __init__.py
        ├── database.py         # Configuración SQLite3, DDL y siembra de datos
        ├── schemas.py          # Modelos DTOs de Pydantic v2 y enumeraciones
        ├── crud.py             # Operaciones SQL nativas (Capa de persistencia)
        ├── main.py             # Instancia principal de FastAPI y documentación
        └── routes/
            ├── __init__.py
            ├── remitentes.py   # APIRouter para gestión de Remitentes
            └── radicados.py    # APIRouter para gestión de Radicados

```

---

##
 Equipo de Desarrollo y Distribución de Funciones

La construcción y el control de versiones del proyecto se organizaron mediante ramas (`feature/`) y commits atribuidos a cada integrante del equipo:

| Integrante | Rama Git | Módulo Asignado | Responsabilidad y Función |
| --- | --- | --- | --- |
| **Integrante 1** | `feature/database-setup` | `database.py`, `requirements.txt` | Conexión SQLite3 nativa, configuración de DDL para tablas, claves foráneas y función `seed_db()` para datos iniciales. |
| **Integrante 2** | `feature/pydantic-schemas` | `schemas.py` | Definición de enumeraciones (`TipoRadicadoEnum`, `EstadoRadicadoEnum`) y validaciones DTO con Pydantic v2. |
| **Integrante 3** | `feature/crud-operations` | `crud.py` | Implementación de la capa de acceso a datos con consultas SQL preparadas (CRUD) para Remitentes y Radicados. |
| **Integrante 4** | `feature/api-routes` | `routes/`, `main.py` | Enrutamiento modular HTTP mediante `APIRouter`, gestión de excepciones HTTP y punto de entrada de FastAPI. |

---

## Tecnologías Utilizadas

* **Python 3.10+**
* **FastAPI:** Framework web asíncrono para la construcción de APIs.
* **Pydantic v2:** Validación de datos y gestión de esquemas.
* **SQLite3:** Motor de base de datos relacional nativo.
* **Uvicorn:** Servidor ASGI para ejecución del entorno de desarrollo.

---

## Instalación y Puesta en Marcha

### 1. Clonar el repositorio

```bash
git clone [https://github.com/TU_USUARIO/REPOSIRORIO.git](https://github.com/TU_USUARIO/REPOSIRORIO.git)
cd ciencia-datos-python

```

### 2. Crear y activar un entorno virtual

```bash
# En Windows:
python -m venv venv
.\venv\Scripts\activate

# En Linux / macOS:
python3 -m venv venv
source venv/bin/activate

```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt

```

### 4. Iniciar el servidor de desarrollo

```bash
uvicorn scripts.correspondencia.main:app --reload

```

---

## Documentación Interactiva (Swagger UI)

Una vez iniciado el servidor, accede a la documentación automática enviando solicitudes HTTP desde el navegador:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

---

