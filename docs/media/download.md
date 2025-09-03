# Endpoint: Descarga de Medios

## 1. Descripción general

El endpoint `/v1/BETA/media/download` permite descargar contenido multimedia de distintas fuentes online usando **yt-dlp**.
Soporta descarga de videos, extracción de audio, obtención de miniaturas y subtítulos.
El procesamiento se gestiona en cola para evitar bloqueos en la aplicación principal.

---

## 2. Endpoint

* **Ruta:** `/v1/BETA/media/download`
* **Método:** `POST`
* **Blueprint:** `v1_media_download_bp`

---

## 3. Petición

### Cabeceras

* `x-api-key` (obligatorio): clave de autenticación.
* `Content-Type`: `application/json`

### Parámetros obligatorios

* `media_url` (string, URI): URL del contenido a descargar.

### Parámetros opcionales

* `webhook_url` (string, URI): URL para recibir resultado al finalizar.
* `id` (string): identificador personalizado.
* `cookie` (string): cookies en formato Netscape, archivo o URL.
* `cloud_upload` (boolean): por defecto `true`. Si es `false`, devuelve URL directo de descarga.

#### Opciones de formato

```json
"format": {
  "quality": "best",
  "format_id": "22",
  "resolution": "720p",
  "video_codec": "string",
  "audio_codec": "string"
}
```

#### Opciones de audio

```json
"audio": {
  "extract": true,
  "format": "mp3",
  "quality": "high"
}
```

#### Opciones de miniaturas

```json
"thumbnails": {
  "download": true,
  "download_all": false,
  "formats": ["jpg"],
  "convert": false,
  "embed_in_audio": false
}
```

#### Opciones de subtítulos

```json
"subtitles": {
  "download": true,
  "languages": ["es", "en"],
  "format": "srt",
  "cloud_upload": true
}
```

#### Opciones de descarga

```json
"download": {
  "max_filesize": 104857600,
  "rate_limit": "50K",
  "retries": 3
}
```

### Ejemplo de petición

```json
{
  "media_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "webhook_url": "https://example.com/webhook",
  "id": "peticion-123",
  "cloud_upload": true,
  "format": { "quality": "best", "resolution": "720p" },
  "audio": { "extract": true, "format": "mp3" },
  "thumbnails": { "download": true },
  "subtitles": { "download": true, "languages": ["es"], "format": "srt" }
}
```

---

## 4. Respuesta

### Respuesta inmediata (con webhook)

```json
{
  "code": 202,
  "id": "peticion-123",
  "job_id": "uuid-job",
  "message": "processing",
  "pid": 12345,
  "queue_id": 67890,
  "max_queue_length": "unlimited",
  "queue_length": 3,
  "build_number": "1.0.123"
}
```

### Respuesta de éxito

```json
{
  "code": 200,
  "id": "peticion-123",
  "job_id": "uuid-job",
  "response": {
    "media": {
      "media_url": "https://storage.example.com/video.mp4",
      "title": "Título del video",
      "ext": "mp4",
      "resolution": "720p",
      "filesize": 12345678,
      "duration": 212
    },
    "thumbnails": [
      {
        "id": "default",
        "image_url": "https://storage.example.com/thumbnail.jpg"
      }
    ]
  },
  "message": "success",
  "pid": 12345,
  "queue_id": 67890,
  "run_time": 5.123,
  "queue_time": 0.456,
  "total_time": 5.579,
  "queue_length": 2,
  "build_number": "1.0.123"
}
```

### Ejemplo de error

```json
{
  "code": 400,
  "id": "peticion-123",
  "message": "Invalid request: 'media_url' is a required property"
}
```

---

## 5. Manejo de errores

* Parámetros faltantes o inválidos → 400
* API key inválida o ausente → 401
* Cola llena → 429
* Fallos en descarga → 500
* Restricciones de fuente (ej. geo-bloqueo) → 500

---

## 6. Notas de uso

* Con `webhook_url`, la tarea se procesa de forma asíncrona.
* Sin `webhook_url`, la petición puede tardar más (síncrona).
* `format` permite controlar calidad y códecs.
* `audio.extract` extrae y convierte a formato elegido.
* `thumbnails.download_all` recupera todas las miniaturas.
* `download.rate_limit` ayuda a evitar bloqueos de IP.

---

## 7. Problemas comunes

* Contenido restringido por región.
* Bloqueo o *rate limiting* de la fuente.
* Archivos muy grandes → *timeout*.
* Formatos solicitados no disponibles.
* Webhook inaccesible → no llega resultado.
* Cola saturada.

---

## 8. Buenas prácticas

* Usar siempre `webhook_url` para descargas largas.
* Especificar formatos concretos para evitar archivos innecesariamente grandes.
* Pedir miniaturas solo cuando sea necesario.
* Implementar reintentos en el cliente.
* Revisar `queue_length` en las respuestas.
* Guardar los archivos descargados rápido (URLs en la nube pueden caducar).
