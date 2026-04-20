# URL Shortener API

Una API RESTful para acortar URLs, construida con FastAPI y SQLAlchemy. Permite crear, redirigir, estadísticas, búsqueda y eliminación de URLs.

## Tecnologías

- **FastAPI**: Framework web moderno para APIs.
- **SQLAlchemy**: ORM para base de datos.
- **SQLite**: Base de datos ligera.
- **Pydantic**: Validación de datos.

## Estructura del Proyecto

```
url-shortener-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # Punto de entrada
│   ├── database.py      # Configuración DB
│   ├── models.py        # Modelos SQLAlchemy
│   ├── schemas.py       # Esquemas Pydantic
│   └── routers/
│       └── url.py       # Rutas de la API
├── requirements.txt
├── README.md
└── urls.db              # Base de datos (generada)
```

## Instalación y Ejecución

1. Clona el repo:
   ```bash
   git clone <url-del-repo>
   cd url-shortener-api
   ```

2. Crea entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
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

## Endpoints

### Crear URL corta
- **POST** `/api/shorten`
- Body: `{"original_url": "https://example.com"}`
- Respuesta: `{"short_url": "http://localhost:8000/api/XyZaBc"}`

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
- Respuesta: `{"short_url": "http://localhost:8000/api/mycustom"}`

## Desarrollo

- La DB se crea automáticamente al iniciar.
- Usa `.env` para configuración (opcional).
- Pruebas con Postman o curl.

## Licencia

MIT