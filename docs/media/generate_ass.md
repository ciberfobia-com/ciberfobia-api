# Endpoint de Generación de Subtítulos ASS (v1)

## 1. Descripción

El endpoint `/v1/media/generate/ass` genera un archivo de subtítulos en formato **ASS (Advanced SubStation Alpha)** a partir de un archivo multimedia (video o audio).
Permite aplicar configuraciones de estilo, exclusión de rangos de tiempo y reemplazos de texto.
El archivo generado se sube a un almacenamiento en la nube y devuelve su URL.

---

## 2. Endpoint

* **URL:** `/v1/media/generate/ass`
* **Método:** `POST`

---

## 3. Petición

### Headers

* `x-api-key` (obligatorio): Clave de autenticación.

### Parámetros del body (JSON)

* `media_url` (string, obligatorio): URL del archivo multimedia.
* `canvas_width` (integer, opcional): Ancho del lienzo en píxeles (recomendado para audio).
* `canvas_height` (integer, opcional): Alto del lienzo en píxeles (recomendado para audio).
* `settings` (object, opcional): Configuración de estilo (colores, fuente, posición, tamaño, estilo de subtítulo).
* `replace` (array, opcional): Lista de reemplazos de texto `{find, replace}`.
* `exclude_time_ranges` (array, opcional): Rangos de tiempo a excluir (`start`, `end` en formato `hh:mm:ss.ms`).
* `language` (string, opcional): Idioma (`en`, `es`, etc.). Por defecto `auto`.
* `webhook_url` (string, opcional): URL de webhook para respuesta asíncrona.
* `id` (string, opcional): Identificador de la petición.

### Ejemplos de petición

**Básico**

```json
{
  "media_url": "https://example.com/video.mp4"
}
```

**Con estilo personalizado**

```json
{
  "media_url": "https://example.com/video.mp4",
  "settings": {
    "style": "classic",
    "line_color": "#FFFFFF",
    "outline_color": "#000000",
    "position": "bottom_center",
    "alignment": "center",
    "font_family": "Arial",
    "font_size": 24,
    "bold": true
  }
}
```

**Karaoke con reemplazos**

```json
{
  "media_url": "https://example.com/video.mp4",
  "settings": {
    "style": "karaoke",
    "line_color": "#FFFFFF",
    "word_color": "#FFFF00",
    "outline_color": "#000000",
    "font_family": "Arial",
    "font_size": 24
  },
  "replace": [
    {"find": "um", "replace": ""},
    {"find": "like", "replace": ""}
  ],
  "id": "req-123",
  "language": "en",
  "webhook_url": "https://example.com/webhook"
}
```

**Excluyendo rangos**

```json
{
  "media_url": "https://example.com/video.mp4",
  "exclude_time_ranges": [
    {"start": "00:00:10.000", "end": "00:00:20.000"},
    {"start": "00:00:30.000", "end": "00:00:40.000"}
  ]
}
```

---

## 4. Respuesta

### Éxito

```json
{
  "code": 200,
  "id": "req-123",
  "job_id": "uuid",
  "response": "https://cloud.example.com/subtitles.ass",
  "message": "success",
  "pid": 12345,
  "queue_id": 6789,
  "run_time": 2.345,
  "queue_time": 0.010,
  "total_time": 2.355,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Errores

**400 – Parámetros inválidos**

```json
{
  "code": 400,
  "message": "Missing or invalid parameters"
}
```

**400 – Fuente no disponible**

```json
{
  "code": 400,
  "error": "The requested font 'InvalidFont' is not available.",
  "available_fonts": ["Arial", "Times New Roman", "Courier New"]
}
```

**401 – Autenticación fallida**

```json
{
  "code": 401,
  "message": "Invalid API key"
}
```

**429 – Cola llena**

```json
{
  "code": 429,
  "message": "MAX_QUEUE_LENGTH reached"
}
```

**500 – Error interno**

```json
{
  "code": 500,
  "message": "An unexpected error occurred"
}
```

---

## 5. Notas de uso

* `canvas_width` y `canvas_height` son obligatorios si el archivo es solo audio.
* `settings` permite personalizar colores, fuente, tamaño, alineación y estilos (`classic`, `karaoke`, `highlight`, `underline`, `word_by_word`).
* `replace` es útil para limpiar muletillas o censurar palabras.
* `webhook_url` permite procesar en segundo plano.