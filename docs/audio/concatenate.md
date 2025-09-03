# Documentación del Endpoint de Concatenación de Audio

## Descripción general

El endpoint `/v1/audio/concatenate` permite combinar múltiples archivos de audio en un único archivo. Forma parte de la estructura de la API v1 y está registrado en la aplicación principal mediante el *Blueprint* `v1_audio_concatenate_bp`. Utiliza el sistema de colas de la aplicación para gestionar el procesamiento de manera asíncrona, lo cual es especialmente útil para operaciones de audio que consumen mucho tiempo.

## Endpoint

- **URL**: `/v1/audio/concatenate`
- **Método**: `POST`

## Petición

### Cabeceras

- `x-api-key`: Obligatorio. Tu clave de autenticación de la API.

### Parámetros en el cuerpo

| Parámetro     | Tipo   | Obligatorio | Descripción |
|---------------|--------|-------------|-------------|
| `audio_urls`  | Array  | Sí          | Un array de objetos, cada uno con la propiedad `audio_url` apuntando a un archivo de audio a concatenar. Debe contener al menos un elemento. |
| `webhook_url` | String | No          | Una URL para recibir notificación de callback cuando el procesamiento finalice. Si se proporciona, la petición será procesada de forma asíncrona. |
| `id`          | String | No          | Identificador personalizado para rastrear la petición. |

Cada objeto dentro del array `audio_urls` debe tener:
- `audio_url`: String (formato URI). La URL de un archivo de audio a concatenar.

### Ejemplo de petición

```json
{
  "audio_urls": [
    { "audio_url": "https://example.com/audio1.mp3" },
    { "audio_url": "https://example.com/audio2.mp3" },
    { "audio_url": "https://example.com/audio3.mp3" }
  ],
  "webhook_url": "https://your-webhook-endpoint.com/callback",
  "id": "custom-request-id-123"
}
````

### Ejemplo con cURL

```bash
curl -X POST \
  https://api.example.com/v1/audio/concatenate \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: your-api-key-here' \
  -d '{
    "audio_urls": [
      { "audio_url": "https://example.com/audio1.mp3" },
      { "audio_url": "https://example.com/audio2.mp3" }
    ],
    "webhook_url": "https://your-webhook-endpoint.com/callback",
    "id": "custom-request-id-123"
  }'
```

## Respuesta

### Respuesta sincrónica (sin `webhook_url`)

```json
{
  "code": 200,
  "id": "custom-request-id-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "https://storage.example.com/combined-audio-file.mp3",
  "message": "success",
  "run_time": 2.345,
  "queue_time": 0,
  "total_time": 2.345,
  "pid": 12345,
  "queue_id": 67890,
  "queue_length": 0,
  "build_number": "1.0.123"
}
```

### Respuesta asincrónica (con `webhook_url`)

```json
{
  "code": 202,
  "id": "custom-request-id-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "processing",
  "pid": 12345,
  "queue_id": 67890,
  "max_queue_length": "unlimited",
  "queue_length": 1,
  "build_number": "1.0.123"
}
```

Cuando el procesamiento termine, se enviará un webhook a la URL proporcionada con este payload:

```json
{
  "endpoint": "/v1/audio/concatenate",
  "code": 200,
  "id": "custom-request-id-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "https://storage.example.com/combined-audio-file.mp3",
  "message": "success",
  "pid": 12345,
  "queue_id": 67890,
  "run_time": 3.456,
  "queue_time": 1.234,
  "total_time": 4.690,
  "queue_length": 0,
  "build_number": "1.0.123"
}
```

### Errores comunes

#### Formato de petición inválido (400 Bad Request)

```json
{
  "code": 400,
  "id": null,
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Invalid request: 'audio_urls' is a required property",
  "pid": 12345,
  "queue_id": 67890,
  "queue_length": 0,
  "build_number": "1.0.123"
}
```

#### Error de autenticación (401 Unauthorized)

```json
{
  "code": 401,
  "message": "Invalid or missing API key",
  "build_number": "1.0.123"
}
```

#### Límite de cola alcanzado (429 Too Many Requests)

```json
{
  "code": 429,
  "id": "custom-request-id-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "MAX_QUEUE_LENGTH (100) reached",
  "pid": 12345,
  "queue_id": 67890,
  "queue_length": 100,
  "build_number": "1.0.123"
}
```

#### Error en el procesamiento (500 Internal Server Error)

```json
{
  "code": 500,
  "id": "custom-request-id-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Error downloading audio file: Connection refused",
  "pid": 12345,
  "queue_id": 67890,
  "queue_length": 0,
  "build_number": "1.0.123"
}
```

## Manejo de errores

* **Parámetros faltantes**: si `audio_urls` falta o está vacío, se devuelve 400.
* **Formato de URL inválido**: si algún `audio_url` no es un URI válido, se devuelve 400.
* **Error de autenticación**: si la API key es inválida o falta, se devuelve 401.
* **Cola llena**: si se supera el límite de cola, se devuelve 429.
* **Errores de procesamiento**: fallos en descarga, procesamiento o subida devuelven 500.

## Notas de uso

1. Para archivos largos, usa `webhook_url` (procesamiento asíncrono).
2. Se admiten formatos de audio comunes, salida típica en MP3.
3. Puede haber límites de tamaño de archivo.
4. Con carga alta, se encolarán las peticiones con webhook.

## Problemas comunes

1. **URLs inaccesibles** → deben ser públicas.
2. **Formatos incompatibles** → usar MP3, WAV, AAC.
3. **Fallos en el webhook** → si tu endpoint no responde, no recibirás la notificación.
4. **Timeouts** → archivos grandes pueden fallar al descargar/procesar.

## Buenas prácticas

1. Usa siempre webhook para archivos grandes o muchos ficheros.
2. Incluye un parámetro `id` para rastrear tus peticiones.
3. Maneja errores en cliente según códigos HTTP.
4. Asegura que tu endpoint de webhook sea fiable.
5. Prepara los audios con formatos y parámetros compatibles.
6. Monitorea `queue_length` para ver la carga del sistema.