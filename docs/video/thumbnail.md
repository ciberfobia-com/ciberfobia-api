# API de Generación de Miniaturas de Video

## Descripción

El endpoint `/v1/video/thumbnail` permite extraer una imagen en miniatura desde un momento específico de un video. El proceso se gestiona de forma asíncrona mediante un sistema de colas, se sube la miniatura generada a un almacenamiento en la nube y se devuelve la URL resultante.

## Endpoint

* **URL**: `/v1/video/thumbnail`
* **Método**: `POST`

## Petición

### Cabeceras

* `x-api-key`: Requerido. Clave de autenticación de la API.

### Parámetros del cuerpo

| Parámetro     | Tipo               | Requerido | Descripción                                                   |
| ------------- | ------------------ | --------- | ------------------------------------------------------------- |
| `video_url`   | string (URI)       | Sí        | URL del video del que se extraerá la miniatura                |
| `second`      | number (mínimo: 0) | No        | Momento en segundos para extraer la miniatura (por defecto 0) |
| `webhook_url` | string (URI)       | No        | URL para recibir el resultado de forma asíncrona              |
| `id`          | string             | No        | Identificador personalizado para seguimiento                  |

### Ejemplo de petición

```json
{
  "video_url": "https://example.com/video.mp4",
  "second": 30,
  "webhook_url": "https://your-service.com/webhook",
  "id": "custom-request-123"
}
```

### Ejemplo cURL

```bash
curl -X POST \
  https://api.example.com/v1/video/thumbnail \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: your-api-key' \
  -d '{
    "video_url": "https://example.com/video.mp4",
    "second": 30,
    "webhook_url": "https://your-service.com/webhook",
    "id": "custom-request-123"
  }'
```

## Respuesta

### Respuesta inmediata (202 Accepted)

Cuando se proporciona un `webhook_url`:

```json
{
  "code": 202,
  "id": "custom-request-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "processing",
  "pid": 12345,
  "queue_id": 67890,
  "max_queue_length": "unlimited",
  "queue_length": 1,
  "build_number": "1.0.0"
}
```

### Respuesta exitosa (200 OK)

Cuando no hay webhook o cuando se envía tras completarse el proceso:

```json
{
  "code": 200,
  "id": "custom-request-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "https://storage.example.com/thumbnails/video-thumbnail-123.jpg",
  "message": "success",
  "run_time": 1.234,
  "queue_time": 0.567,
  "total_time": 1.801,
  "pid": 12345,
  "queue_id": 67890,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Errores

**400 Petición inválida**

```json
{
  "code": 400,
  "message": "Invalid request: 'video_url' is a required property",
  "job_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**429 Cola llena**

```json
{
  "code": 429,
  "id": "custom-request-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "MAX_QUEUE_LENGTH (100) reached",
  "pid": 12345,
  "queue_id": 67890,
  "queue_length": 100,
  "build_number": "1.0.0"
}
```

**500 Error interno**

```json
{
  "code": 500,
  "id": "custom-request-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Failed to download video from provided URL",
  "pid": 12345,
  "queue_id": 67890,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

## Manejo de errores

* Falta de parámetros requeridos → 400
* Formato inválido (URLs incorrectas, etc.) → 400
* Cola llena → 429
* Errores de procesamiento → 500

## Notas de uso

1. Procesamiento asíncrono con `webhook_url` recomendado para operaciones largas.
2. El parámetro `second` debe ser un valor adecuado para capturar un frame representativo.
3. Usar `id` para rastrear solicitudes.
4. Revisar `MAX_QUEUE_LENGTH` para gestión de carga.

## Problemas comunes

* URLs inaccesibles.
* `second` mayor que la duración del video.
* Fallo del webhook de cliente.
* Videos muy grandes → mayor tiempo de espera.

## Buenas prácticas

* Usar webhooks en videos largos.
* Seleccionar timestamps representativos.
* Implementar manejo de errores en cliente.
* Vigilar longitud de cola para evitar saturación.
* Usar `id` para solicitudes idempotentes.
