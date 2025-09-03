# Documentación de la API de Transcripción de Medios

## Descripción

El endpoint de transcripción de medios forma parte de la API v1, proporcionando transcripción y traducción de audio/vídeo. Utiliza un sistema de colas para manejar tareas largas, con soporte de webhooks para procesamiento asíncrono. Está integrado en la aplicación Flask principal como un *Blueprint* y soporta tanto respuestas directas como almacenamiento en la nube para los resultados.

## Endpoint

* **URL**: `/v1/media/transcribe`
* **Método**: `POST`
* **Blueprint**: `v1_media_transcribe_bp`

## Request

### Headers

* `x-api-key`: Requerido. Clave de autenticación para acceso.
* `Content-Type`: Requerido. Debe ser `application/json`.

### Parámetros del cuerpo

#### Requeridos

* `media_url` (string)

  * Formato: URI
  * Descripción: URL del archivo multimedia a transcribir

#### Opcionales

* `task` (string)

  * Valores permitidos: `"transcribe"`, `"translate"`
  * Por defecto: `"transcribe"`
  * Especifica si se debe transcribir o traducir el audio

* `include_text` (boolean)

  * Por defecto: `true`
  * Incluir transcripción en texto plano en la respuesta

* `include_srt` (boolean)

  * Por defecto: `false`
  * Incluir subtítulos en formato SRT

* `include_segments` (boolean)

  * Por defecto: `false`
  * Incluir segmentos con marcas de tiempo

* `word_timestamps` (boolean)

  * Por defecto: `false`
  * Incluir marcas de tiempo para cada palabra

* `response_type` (string)

  * Valores: `"direct"`, `"cloud"`
  * Por defecto: `"direct"`
  * Indica si devolver los resultados directamente o como URLs en la nube

* `language` (string)

  * Idioma de origen para la transcripción

* `webhook_url` (string)

  * Formato: URI
  * URL para recibir resultados de forma asíncrona

* `id` (string)

  * Identificador personalizado para el trabajo

* `max_words_per_line` (integer)

  * Mínimo: 1
  * Controla el número máximo de palabras por línea en el SRT

### Ejemplo de request

```bash
curl -X POST "https://api.example.com/v1/media/transcribe" \
  -H "x-api-key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "media_url": "https://example.com/media/file.mp3",
    "task": "transcribe",
    "include_text": true,
    "include_srt": true,
    "include_segments": true,
    "response_type": "cloud",
    "webhook_url": "https://your-webhook.com/callback",
    "id": "custom-job-123",
    "max_words_per_line": 5
  }'
```

## Response

### Respuesta inmediata (202 Accepted)

Con `webhook_url`:

```json
{
  "code": 202,
  "id": "custom-job-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "processing",
  "pid": 12345,
  "queue_id": 67890,
  "max_queue_length": "unlimited",
  "queue_length": 1,
  "build_number": "1.0.0"
}
```

### Respuesta exitosa (directa)

```json
{
  "endpoint": "/v1/transcribe/media",
  "code": 200,
  "id": "custom-job-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": {
    "text": "Texto transcrito...",
    "srt": "Contenido en SRT...",
    "segments": [...],
    "text_url": null,
    "srt_url": null,
    "segments_url": null
  },
  "message": "success",
  "pid": 12345,
  "queue_id": 67890,
  "run_time": 5.234,
  "queue_time": 0.123,
  "total_time": 5.357,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Respuesta exitosa (cloud)

```json
{
  "endpoint": "/v1/transcribe/media",
  "code": 200,
  "id": "custom-job-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": {
    "text": null,
    "srt": null,
    "segments": null,
    "text_url": "https://storage.example.com/text.txt",
    "srt_url": "https://storage.example.com/subtitles.srt",
    "segments_url": "https://storage.example.com/segments.json"
  },
  "message": "success",
  "pid": 12345,
  "queue_id": 67890,
  "run_time": 5.234,
  "queue_time": 0.123,
  "total_time": 5.357,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Errores

#### Cola llena (429)

```json
{
  "code": 429,
  "id": "custom-job-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "MAX_QUEUE_LENGTH (100) reached",
  "pid": 12345,
  "queue_id": 67890,
  "queue_length": 100,
  "build_number": "1.0.0"
}
```

#### Error interno (500)

```json
{
  "endpoint": "/v1/transcribe/media",
  "code": 500,
  "id": "custom-job-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": null,
  "message": "Error message details",
  "pid": 12345,
  "queue_id": 67890,
  "run_time": 0.123,
  "queue_time": 0.056,
  "total_time": 0.179,
  "queue_length": 1,
  "build_number": "1.0.0"
}
```

## Manejo de errores

### Errores comunes

* Clave de API inválida: 401 Unauthorized
* JSON inválido: 400 Bad Request
* Campos requeridos faltantes: 400 Bad Request
* media\_url inválida: 400 Bad Request
* Cola llena: 429 Too Many Requests
* Error de procesamiento: 500 Internal Server Error

### Validación

* URIs inválidas en `media_url` o `webhook_url`
* Valor inválido en `task` o `response_type`
* Propiedades desconocidas en el cuerpo

## Notas de uso

1. **Webhook**: usar `webhook_url` para procesamiento asíncrono.
2. **Cola**: controlada por `MAX_QUEUE_LENGTH`.
3. **Archivos**: en `cloud`, se suben a almacenamiento temporal.
4. **SRT**: `max_words_per_line` controla palabras por línea.

## Problemas comunes

* Archivos inaccesibles o corruptos.
* `webhook_url` no accesible.
* Archivos grandes que requieren más tiempo.

## Buenas prácticas

* Siempre usar `id` único.
* Usar `cloud` para archivos grandes.
* Implementar reintentos en webhooks.
* Usar HTTPS en `media_url` y `webhook_url`.
