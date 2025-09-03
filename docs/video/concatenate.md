# Endpoint de Concatenación de Videos

## 1. Descripción

El endpoint `/v1/video/concatenate` forma parte de la API de Video y permite combinar múltiples archivos de video en un único archivo final. Pertenece al conjunto de rutas versión 1 (v1), bajo el namespace `/v1/video`.

## 2. Endpoint

**Ruta:** `/v1/video/concatenate`  
**Método HTTP:** `POST`

## 3. Request

### Headers

- `x-api-key` (obligatorio): Clave de autenticación.

### Parámetros del Body

El cuerpo debe ser un JSON con la siguiente estructura:

- `video_urls` (obligatorio, array de objetos): Lista de videos a concatenar. Cada objeto debe tener la propiedad `video_url` (string, formato URI).
- `webhook_url` (opcional, string, formato URI): URL a la que se enviará la respuesta vía webhook.
- `id` (opcional, string): Identificador del request.

**Esquema validado:**

```json
{
  "type": "object",
  "properties": {
    "video_urls": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "video_url": {"type": "string", "format": "uri"}
        },
        "required": ["video_url"]
      },
      "minItems": 1
    },
    "webhook_url": {"type": "string", "format": "uri"},
    "id": {"type": "string"}
  },
  "required": ["video_urls"],
  "additionalProperties": false
}
````

### Ejemplo de Request

```json
{
  "video_urls": [
    {"video_url": "https://example.com/video1.mp4"},
    {"video_url": "https://example.com/video2.mp4"},
    {"video_url": "https://example.com/video3.mp4"}
  ],
  "webhook_url": "https://example.com/webhook",
  "id": "request-123"
}
```

```bash
curl -X POST \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_urls": [
      {"video_url": "https://example.com/video1.mp4"},
      {"video_url": "https://example.com/video2.mp4"},
      {"video_url": "https://example.com/video3.mp4"}
    ],
    "webhook_url": "https://example.com/webhook",
    "id": "request-123"
  }' \
  https://your-api-endpoint.com/v1/video/concatenate
```

## 4. Response

### Éxito

```json
{
  "endpoint": "/v1/video/concatenate",
  "code": 200,
  "id": "request-123",
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "response": "https://cloud-storage.example.com/combined-video.mp4",
  "message": "success",
  "pid": 12345,
  "queue_id": 6789,
  "run_time": 10.234,
  "queue_time": 2.345,
  "total_time": 12.579,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

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
  "message": "Unauthorized"
}
```

* **429 Too Many Requests**

```json
{
  "code": 429,
  "id": "request-123",
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
  "message": "An error occurred during video concatenation"
}
```

## 5. Manejo de Errores

* Request inválido → `400 Bad Request`
* API key faltante o inválida → `401 Unauthorized`
* Cola llena (`MAX_QUEUE_LENGTH`) → `429 Too Many Requests`
* Fallos inesperados durante concatenación → `500 Internal Server Error`

## 6. Notas de Uso

* Los videos deben ser accesibles desde las URLs proporcionadas.
* El orden en el array `video_urls` define el orden de concatenación.
* Si se incluye `webhook_url`, la respuesta se enviará a esa dirección.
* El campo `id` sirve para rastrear la petición.

## 7. Problemas Comunes

* URLs inválidas o inaccesibles.
* Exceso de peticiones que llena la cola.
* Errores inesperados de procesamiento.

## 8. Buenas Prácticas

* Validar URLs antes del request.
* Monitorizar la cola y ajustar `MAX_QUEUE_LENGTH`.
* Implementar retries para errores temporales.
* Usar `id` descriptivos para rastreo en logs.