# Endpoint: Conversión de Medios a MP3

## 1. Descripción general

El endpoint `/v1/media/convert/mp3` convierte archivos de audio o video en formato **MP3**.
Está registrado en `app.py` bajo el *blueprint* `v1_media_convert_mp3_bp`.

---

## 2. Endpoint

```
POST /v1/media/convert/mp3
```

---

## 3. Petición

### Cabeceras

* `x-api-key` (obligatorio): clave de autenticación.

### Parámetros en el cuerpo

* `media_url` (string, obligatorio): URL del archivo a convertir.
* `webhook_url` (string, opcional): URL para recibir notificación al finalizar.
* `id` (string, opcional): identificador único de la petición.
* `bitrate` (string, opcional): bitrate deseado en formato `<valor>k` (ej. `128k`). Por defecto `128k`.

**Esquema de validación:**

```json
{
  "type": "object",
  "properties": {
    "media_url": {"type": "string", "format": "uri"},
    "webhook_url": {"type": "string", "format": "uri"},
    "id": {"type": "string"},
    "bitrate": {"type": "string", "pattern": "^[0-9]+k$"}
  },
  "required": ["media_url"],
  "additionalProperties": false
}
```

### Ejemplo de petición

```json
{
  "media_url": "https://example.com/video.mp4",
  "webhook_url": "https://example.com/webhook",
  "id": "peticion-123",
  "bitrate": "192k"
}
```

Ejemplo con cURL:

```bash
curl -X POST \
  -H "x-api-key: TU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"media_url": "https://example.com/video.mp4", "webhook_url": "https://example.com/webhook", "id": "peticion-123", "bitrate": "192k"}' \
  https://tu-api/v1/media/convert/mp3
```

---

## 4. Respuesta

### Ejemplo de éxito

```json
{
  "endpoint": "/v1/media/convert/mp3",
  "code": 200,
  "id": "peticion-123",
  "job_id": "uuid-job",
  "response": "https://cloud-storage.example.com/converted-file.mp3",
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

### Ejemplo de error

```json
{
  "code": 400,
  "id": "peticion-123",
  "job_id": "uuid-job",
  "message": "Invalid request payload: 'media_url' is a required property",
  "pid": 12345,
  "queue_id": 6789,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

---

## 5. Manejo de errores

* Parámetro `media_url` faltante o inválido → 400
* `bitrate` inválido → 400
* API key inválida o ausente → 401
* Error interno inesperado → 500
* Cola llena → 429

---

## 6. Notas de uso

* `media_url` debe ser accesible y válido.
* `bitrate` permite ajustar la calidad de salida, por defecto 128k.
* `webhook_url` es útil para recibir notificaciones al finalizar.
* `id` ayuda al seguimiento y logging.

---

## 7. Problemas comunes

* URL inaccesible o inválida.
* Formato no soportado.
* Cola llena → 429.

---

## 8. Buenas prácticas

* Validar `media_url` antes de enviar.
* Usar `webhook_url` para evitar *polling*.
* Generar `id` únicos para cada petición.
* Implementar reintentos en caso de errores temporales.
* Monitorizar logs de la API.