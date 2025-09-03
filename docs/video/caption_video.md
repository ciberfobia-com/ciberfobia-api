# Endpoint de Subtítulos en Video (v1)

## 1. Descripción

El endpoint `/v1/video/caption` pertenece a la Video API y se encarga de añadir subtítulos a un archivo de video. Acepta la URL del video, el texto de subtítulos (o un archivo SRT/ASS externo) y opciones de estilo. Utiliza el servicio `process_captioning_v1` para generar el video con subtítulos, lo sube al almacenamiento en la nube y devuelve la URL resultante.

## 2. Endpoint

* **URL:** `/v1/video/caption`
* **Método:** `POST`

## 3. Request

### Headers

* `x-api-key` (**requerido**): clave API de autenticación.

### Body

* `video_url` (**string, requerido**): URL del video.
* `captions` (**string, opcional**): puede ser texto, URL a un archivo SRT/ASS o nada (se transcribe el audio automáticamente).
* `settings` (**objeto, opcional**): opciones de estilo para subtítulos.
* `replace` (**array, opcional**): lista de objetos `{find, replace}` para sustituir texto.
* `webhook_url` (**string, opcional**): URL webhook para notificación asincrónica.
* `id` (**string, opcional**): identificador del request.
* `language` (**string, opcional**): código de idioma (ej. `"en"`, `"fr"`, por defecto `"auto"`).
* `exclude_time_ranges` (**array, opcional**): intervalos de tiempo a excluir con formato `{start, end}` (`hh:mm:ss.ms`).

#### Esquema de `settings`

```json
{
  "line_color": "string",
  "word_color": "string",
  "outline_color": "string",
  "all_caps": "boolean",
  "max_words_per_line": "integer",
  "x": "integer",
  "y": "integer",
  "position": "bottom_center | top_left | middle_right ...",
  "alignment": "left | center | right",
  "font_family": "string",
  "font_size": "integer",
  "bold": "boolean",
  "italic": "boolean",
  "underline": "boolean",
  "strikeout": "boolean",
  "style": "classic | karaoke | highlight | underline | word_by_word",
  "outline_width": "integer",
  "spacing": "integer",
  "angle": "integer",
  "shadow_offset": "integer"
}
```

### Ejemplos

* **Automático**:

```json
{ "video_url": "https://example.com/video.mp4" }
```

* **Texto con estilo**:

```json
{
  "video_url": "https://example.com/video.mp4",
  "captions": "Texto de ejemplo",
  "settings": { "style": "classic", "font_family": "Arial", "font_size": 24 }
}
```

* **Karaoke avanzado**:

```json
{
  "video_url": "https://example.com/video.mp4",
  "settings": { "style": "karaoke", "word_color": "#FFFF00", "font_size": 24 }
}
```

* **Archivo externo**:

```json
{
  "video_url": "https://example.com/video.mp4",
  "captions": "https://example.com/subs.srt"
}
```

* **Exclusión de tiempos**:

```json
{
  "video_url": "https://example.com/video.mp4",
  "exclude_time_ranges": [
    {"start": "00:00:10.000", "end": "00:00:20.000"}
  ]
}
```

## 4. Response

### Éxito (200 OK)

```json
{
  "code": 200,
  "id": "request-123",
  "job_id": "uuid-job",
  "response": "https://cloud.example.com/captioned-video.mp4",
  "message": "success",
  "pid": 12345,
  "queue_id": 140682639937472,
  "run_time": 5.234,
  "queue_time": 0.012,
  "total_time": 5.246,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Errores

* **400 Bad Request**: parámetros faltantes o inválidos.
* **400 Font Error**: fuente no disponible → devuelve lista de fuentes válidas.
* **429 Too Many Requests**: cola saturada.
* **500 Internal Server Error**: error inesperado en el proceso.

## 5. Manejo de Errores

* Parámetros inválidos → 400.
* Fuente inexistente → 400 con fuentes disponibles.
* Excepción en el proceso → 500.
* Cola llena → 429.

## 6. Notas de Uso

* `captions` admite texto, archivo SRT, archivo ASS o transcripción automática.
* Estilos avanzados (`karaoke`, `word_by_word`, etc.) disponibles solo con texto/ASS.
* Para SRT solo se soporta estilo `classic`.
* `replace` útil para limpiar o censurar palabras.

## 7. Problemas Comunes

* URL inválida/inaccesible.
* Fuente solicitada no existe.
* Cola saturada.

## 8. Buenas Prácticas

* Validar `video_url` antes de enviar.
* Usar `webhook_url` en lugar de hacer polling.
* Proporcionar `id` descriptivo para seguimiento.
* Cachear videos subtitulados frecuentes.
