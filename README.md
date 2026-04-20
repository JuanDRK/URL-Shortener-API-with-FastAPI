# URL Shortener API

Una API RESTful para acortar URLs, construida con FastAPI y SQLAlchemy. Permite crear, redirigir, estadísticas, búsqueda y eliminación de URLs.

## Tecnologías

- **FastAPI**: Framework web moderno para APIs.
- **SQLAlchemy**: ORM para base de datos.
- **SQLite**: Base de datos ligera.
- **Pydantic**: Validación de datos.
- **Pytest**: Pruebas automatizadas.

## Estructura del Proyecto

```
url-shortener-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada
│   ├── core/
│   │   └── config.py           # Variables de entorno y settings
│   ├── db/
│   │   ├── database.py         # Configuración de conexión y sesión
│   │   └── models.py           # Modelos SQLAlchemy
│   ├── schemas/
│   │   └── url.py              # Esquemas Pydantic
│   └── api/
│       └── v1/
│           └── routers/
│               └── url.py      # Endpoints de URL Shortener
├── tests/
│   └── test_url_api.py
├── requirements.txt
├── README.md
└── urls.db              # Base de datos (generada)
```

## Instalación y Ejecución

Recomendado: Python 3.10+.

1. Clona el repo:
   ```bash
   git clone <url-del-repo>
   cd url-shortener-api
   ```

2. Crea entorno virtual:
   ```bash
   python -m venv .venv
   # Linux/macOS
   source .venv/bin/activate
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   ```

3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la API:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Abre en navegador: `http://127.0.0.1:8000/docs` (Swagger UI).

6. Ejecuta pruebas:
   ```bash
   python -m pytest
   ```

## Endpoints

### Health check
- **GET** `/`
- Respuesta: `{"status": "ok", "service": "url-shortener-api"}`

### Crear URL corta
- **POST** `/api/shorten`
- Body: `{"original_url": "https://example.com"}`
- Respuesta: `{"short_url": "http://127.0.0.1:8000/api/XyZaBc"}`

### Redirigir
- **GET** `/api/{code}`
- Redirige a la URL original.

### Estadísticas
- **GET** `/api/stats/{code}`
- Respuesta: `{"original_url": "https://example.com", "clicks": 5}`

### Top URLs
- **GET** `/api/top`
- Respuesta: Lista de top 5 por clicks.

### Buscar URLs
- **GET** `/api/search?q=example`
- Respuesta: Lista de URLs que contienen "example".

### Eliminar URL
- **DELETE** `/api/urls/{code}`
- Respuesta: `{"message": "Deleted"}`

### Código personalizado
- **POST** `/api/custom`
- Body: `{"original_url": "https://example.com", "custom_code": "mycustom"}`
- Respuesta: `{"short_url": "http://127.0.0.1:8000/api/mycustom"}`
- Reglas `custom_code`: 3-32 caracteres, solo `a-z`, `A-Z`, `0-9`, `_`, `-`.

## Desarrollo

- La DB se crea automáticamente al iniciar.
- Usa `.env` para configuración (opcional), ejemplo:
  - `DATABASE_URL=sqlite:///./urls.db`
- Pruebas automáticas disponibles con `pytest`.

## Licencia

MIT