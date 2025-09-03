# Endpoint de División de Video

## 1. Descripción general

El endpoint `/v1/video/split` forma parte de la API de Video y se utiliza para dividir un archivo de vídeo en múltiples segmentos según tiempos de inicio y fin especificados. Este endpoint pertenece a las rutas de la versión 1 (`v1`), bajo la categoría `video`.

## 2. Endpoint

```
POST /v1/video/split
```

## 3. Petición

### Cabeceras

* `x-api-key` (obligatorio): Clave de API para autenticación.

### Parámetros del cuerpo

El cuerpo debe ser un objeto JSON con las siguientes propiedades:

* `video_url` (obligatorio, string): URL del vídeo a dividir.
* `splits` (obligatorio, array de objetos): Lista de objetos con inicio y fin de cada corte.

  * `start` (obligatorio, string): Tiempo de inicio en formato `hh:mm:ss.ms`.
  * `end` (obligatorio, string): Tiempo de fin en formato `hh:mm:ss.ms`.
* `video_codec` (opcional, string): Códec de vídeo. Por defecto `libx264`.
* `video_preset` (opcional, string): Preset de codificación. Por defecto `medium`.
* `video_crf` (opcional, number): Factor de calidad (0–51). Por defecto 23.
* `audio_codec` (opcional, string): Códec de audio. Por defecto `aac`.
* `audio_bitrate` (opcional, string): Bitrate de audio. Por defecto `128k`.
* `webhook_url` (opcional, string): URL para notificación al completar.
* `id` (opcional, string): Identificador único de la petición.

### Ejemplo de petición

```json
{
  "video_url": "https://example.com/video.mp4",
  "splits": [
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
  https://api.example.com/v1/video/split \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "video_url": "https://example.com/video.mp4",
    "splits": [
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

```json
{
  "endpoint": "/v1/video/split",
  "code": 200,
  "id": "unique-request-id",
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "response": [
    {
      "file_url": "https://example.com/split-1.mp4"
    },
    {
      "file_url": "https://example.com/split-2.mp4"
    }
  ],
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

El campo `response` contiene una lista de objetos, cada uno con la URL del segmento generado.

### Respuestas de error

* **400 Bad Request**: El cuerpo de la petición es inválido o faltan campos.
* **401 Unauthorized**: Falta o es inválida la cabecera `x-api-key`.
* **429 Too Many Requests**: Se ha alcanzado la longitud máxima de la cola.
* **500 Internal Server Error**: Error inesperado durante el proceso.

Ejemplo:

```json
{
  "code": 400,
  "id": "unique-request-id",
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "message": "Invalid request payload: 'splits' is a required property",
  "pid": 12345,
  "queue_id": 6789,
  "queue_length": 2,
  "build_number": "1.0.0"
}
```

## 5. Manejo de errores

* Parámetros inválidos o faltantes → 400
* Fallo de autenticación → 401
* Cola llena → 429
* Excepción inesperada → 500

## 6. Notas de uso

* `video_url` debe ser una URL válida accesible.
* `splits` debe contener al menos un objeto con `start` y `end`.
* Tiempos deben estar en formato `hh:mm:ss.ms`.
* Parámetros de codificación son opcionales.
* Si se especifica `webhook_url`, se enviará notificación al completar.
* `id` es opcional pero útil para seguimiento.

## 7. Problemas comunes

* URL de vídeo inválida o inaccesible.
* Tiempos solapados o mal definidos en `splits`.
* Cola llena (429).

## 8. Buenas prácticas

* Validar la URL antes de enviar.
* Revisar que los tiempos no se solapen ni excedan la duración del vídeo.
* Usar `webhook_url` en procesos largos.
* Implementar reintentos y gestión de errores en el cliente.
* Monitorizar la cola y ajustar `MAX_QUEUE_LENGTH` según necesidad.
