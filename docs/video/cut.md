# Endpoint de Corte de Video

## 1. Descripción general

El endpoint `/v1/video/cut` forma parte de la API de Video y permite cortar segmentos específicos de un archivo de vídeo con parámetros opcionales de codificación. Este endpoint encaja dentro de la estructura general de la API como parte de las rutas de la versión 1 (`v1`), bajo la categoría `video`.

## 2. Endpoint

```
POST /v1/video/cut
```

## 3. Petición

### Cabeceras

* `x-api-key` (obligatorio): La clave de API para autenticación.

### Parámetros del cuerpo

El cuerpo debe ser un objeto JSON con las siguientes propiedades:

* `video_url` (obligatorio, string): URL del vídeo a cortar.
* `cuts` (obligatorio, array de objetos): Segmentos de corte, cada objeto debe incluir:

  * `start` (obligatorio, string): Tiempo de inicio en formato `hh:mm:ss.ms`.
  * `end` (obligatorio, string): Tiempo de fin en formato `hh:mm:ss.ms`.
* `video_codec` (opcional, string): Códec de vídeo a usar. Por defecto `libx264`.
* `video_preset` (opcional, string): Preset de codificación de vídeo. Por defecto `medium`.
* `video_crf` (opcional, number): Factor de calidad (CRF), entre 0 y 51. Por defecto 23.
* `audio_codec` (opcional, string): Códec de audio. Por defecto `aac`.
* `audio_bitrate` (opcional, string): Bitrate de audio. Por defecto `128k`.
* `webhook_url` (opcional, string): URL para recibir notificación al completar el proceso.
* `id` (opcional, string): Identificador único del request.

### Ejemplo de petición

```json
{
  "video_url": "https://example.com/video.mp4",
  "cuts": [
    {
      "start": "00:00:10.000",
      "end": "00:00:20.000"
    },
    {
      "start": "00:00:30.000",
      "end": "00:00:40.000"
    }
  ],
  "video_codec": "libx264",
  "video_preset": "medium",
  "video_crf": 23,
  "audio_codec": "aac",
  "audio_bitrate": "128k",
  "webhook_url": "https://example.com/webhook",
  "id": "unique-request-id"
}
```

```bash
curl -X POST \
  https://api.example.com/v1/video/cut \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "video_url": "https://example.com/video.mp4",
    "cuts": [
      {
        "start": "00:00:10.000",
        "end": "00:00:20.000"
      },
      {
        "start": "00:00:30.000",
        "end": "00:00:40.000"
      }
    ],
    "video_codec": "libx264",
    "video_preset": "medium",
    "video_crf": 23,
    "audio_codec": "aac",
    "audio_bitrate": "128k",
    "webhook_url": "https://example.com/webhook",
    "id": "unique-request-id"
  }'
```

## 4. Respuesta

### Respuesta exitosa

Ejemplo:

```json
{
  "endpoint": "/v1/video/cut",
  "code": 200,
  "id": "unique-request-id",
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "response": "https://example.com/processed-video.mp4",
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

El campo `response` contiene la URL del vídeo procesado.

### Errores

* **400 Bad Request**

```json
{
  "code": 400,
  "message": "Invalid request payload"
}
```

* **401 Unauthorized**

```json
{
  "code": 401,
  "message": "Invalid API key"
}
```

* **429 Too Many Requests**

```json
{
  "code": 429,
  "id": "unique-request-id",
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "message": "MAX_QUEUE_LENGTH (100) reached",
  "pid": 12345,
  "queue_id": 6789,
  "queue_length": 100,
  "build_number": "1.0.0"
}
```

* **500 Internal Server Error**

```json
{
  "code": 500,
  "message": "An error occurred during video processing"
}
```

## 5. Manejo de errores

* Parámetros faltantes o inválidos → 400 Bad Request
* API key inválida → 401 Unauthorized
* Cola llena → 429 Too Many Requests
* Errores inesperados en el procesado → 500 Internal Server Error

## 6. Notas de uso

* `video_url` debe ser accesible por el servidor.
* Los segmentos deben estar bien formateados y sin solaparse.
* Los parámetros de codificación afectan calidad y tiempo de proceso.
* Si se pasa `webhook_url`, la notificación llega al completarse el job.
* `id` puede usarse para correlación.

## 7. Problemas comunes

* URL de vídeo no válida o inaccesible.
* Segmentos mal definidos o superpuestos.
* Parámetros de codificación no soportados.
* Cola saturada (429).

## 8. Buenas prácticas

* Validar la URL antes de enviar.
* Revisar que los cortes no excedan la duración del vídeo.
* Ajustar CRF y presets según necesidad de calidad/rendimiento.
* Implementar reintentos para manejar 429.
* Usar `webhook_url` o consultar estado de job para trabajos largos.

¿Quieres que traduzca en bloque también los otros endpoints de `video` que ya vimos (caption, concatenate) para mantener consistencia?