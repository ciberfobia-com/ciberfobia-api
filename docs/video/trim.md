# Endpoint de Recorte de Video

## 1. Descripción

El endpoint `/v1/video/trim` forma parte de la API de Video y permite recortar un video eliminando porciones desde el inicio y/o el final. Ofrece además parámetros opcionales de codificación para controlar la calidad del video de salida.

## 2. Endpoint

**Ruta:** `/v1/video/trim`
**Método HTTP:** `POST`

## 3. Petición

### Cabeceras

* `x-api-key` (requerido): Clave de autenticación.

### Parámetros del cuerpo

* `video_url` (requerido, string): URL del archivo de video a recortar.
* `start` (opcional, string): Tiempo de inicio en formato `hh:mm:ss` o `mm:ss`.
* `end` (opcional, string): Tiempo de fin en formato `hh:mm:ss` o `mm:ss`.
* `video_codec` (opcional, string): Códec de video para la salida. Por defecto `libx264`.
* `video_preset` (opcional, string): Preset de codificación. Por defecto `medium`.
* `video_crf` (opcional, number): Factor CRF (0–51). Por defecto `23`.
* `audio_codec` (opcional, string): Códec de audio. Por defecto `aac`.
* `audio_bitrate` (opcional, string): Bitrate de audio. Por defecto `128k`.
* `webhook_url` (opcional, string): URL para recibir notificación cuando termine el proceso.
* `id` (opcional, string): Identificador único de la petición.

### Ejemplo de petición

```json
{
  "video_url": "https://example.com/video.mp4",
  "start": "00:01:00",
  "end": "00:03:00",
  "video_codec": "libx264",
  "video_preset": "faster",
  "video_crf": 28,
  "audio_codec": "aac",
  "audio_bitrate": "128k",
  "webhook_url": "https://example.com/webhook",
  "id": "unique-request-id"
}
```

```bash
curl -X POST \
  https://api.example.com/v1/video/trim \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "video_url": "https://example.com/video.mp4",
    "start": "00:01:00",
    "end": "00:03:00",
    "video_codec": "libx264",
    "video_preset": "faster",
    "video_crf": 28,
    "audio_codec": "aac",
    "audio_bitrate": "128k",
    "webhook_url": "https://example.com/webhook",
    "id": "unique-request-id"
  }'
```

## 4. Respuesta

### Respuesta exitosa

```json
{
  "endpoint": "/v1/video/trim",
  "code": 200,
  "id": "unique-request-id",
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "response": "https://example.com/trimmed-video.mp4",
  "message": "success",
  "pid": 12345,
  "queue_id": 6789,
  "run_time": 5.234,
  "queue_time": 0.123,
  "total_time": 5.357,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Errores

**400 Petición inválida**

```json
{
  "code": 400,
  "message": "Invalid request payload"
}
```

**401 No autorizado**

```json
{
  "code": 401,
  "message": "Unauthorized"
}
```

**500 Error interno**

```json
{
  "code": 500,
  "message": "An error occurred during the video trimming process"
}
```

## 5. Manejo de errores

* Parámetros ausentes o inválidos → 400
* Clave API inválida → 401
* Cola llena → 429
* Fallo inesperado en el proceso → 500

## 6. Notas de uso

* Se requiere al menos uno de los parámetros `start` o `end`.
* Los parámetros de codificación son opcionales.
* El `webhook_url` permite recibir notificación al finalizar.
* El `id` ayuda a identificar la petición.

## 7. Problemas comunes

* `video_url` inválida o inaccesible.
* Valores no soportados en parámetros de codificación.
* Videos corruptos o en formatos no soportados.

## 8. Buenas prácticas

* Validar `video_url` antes de enviar.
* Ajustar parámetros de codificación según calidad/tamaño deseados.
* Implementar reintentos y control de errores.
* Monitorizar el tamaño de la cola (`MAX_QUEUE_LENGTH`).
* Aplicar limitación de peticiones para evitar abuso.
