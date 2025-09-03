# Conversión de Imagen a Video

## 1. Descripción general

El endpoint `/v1/image/convert/video` convierte una imagen en un archivo de video.
Está registrado en `app.py` bajo el *blueprint* `v1_image_convert_video_bp`, importado desde `routes.v1.image.convert.image_to_video`.

---

## 2. Endpoint

* **Ruta:** `/v1/image/convert/video`
* **Método:** `POST`

---

## 3. Petición

### Cabeceras

* `x-api-key` (obligatorio): clave de autenticación.

### Parámetros en el cuerpo

| Parámetro     | Tipo    | Obligatorio | Descripción                                                   |
| ------------- | ------- | ----------- | ------------------------------------------------------------- |
| `image_url`   | string  | Sí          | URL de la imagen a convertir en video.                        |
| `length`      | number  | No          | Duración del video en segundos (por defecto: 5).              |
| `frame_rate`  | integer | No          | Fotogramas por segundo del video de salida (por defecto: 30). |
| `zoom_speed`  | number  | No          | Velocidad del efecto de zoom (0-100, por defecto: 3).         |
| `webhook_url` | string  | No          | URL para recibir notificación al finalizar.                   |
| `id`          | string  | No          | Identificador opcional de la petición.                        |

**Esquema de validación:**

```json
{
  "type": "object",
  "properties": {
    "image_url": {"type": "string", "format": "uri"},
    "length": {"type": "number", "minimum": 1, "maximum": 60},
    "frame_rate": {"type": "integer", "minimum": 15, "maximum": 60},
    "zoom_speed": {"type": "number", "minimum": 0, "maximum": 100},
    "webhook_url": {"type": "string", "format": "uri"},
    "id": {"type": "string"}
  },
  "required": ["image_url"],
  "additionalProperties": false
}
```

### Ejemplo de petición

```json
{
  "image_url": "https://example.com/image.jpg",
  "length": 10,
  "frame_rate": 24,
  "zoom_speed": 5,
  "webhook_url": "https://example.com/webhook",
  "id": "request-123"
}
```

Ejemplo con cURL:

```bash
curl -X POST \
  -H "x-api-key: TU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/image.jpg", "length": 10, "frame_rate": 24, "zoom_speed": 5, "webhook_url": "https://example.com/webhook", "id": "request-123"}' \
  http://tu-api/v1/image/convert/video
```

---

## 4. Respuesta

### Ejemplo de éxito

```json
{
  "code": 200,
  "id": "request-123",
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "response": "https://cloud-storage.example.com/converted-video.mp4",
  "message": "success",
  "run_time": 2.345,
  "queue_time": 0.123,
  "total_time": 2.468,
  "pid": 12345,
  "queue_id": 1234567890,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Ejemplo de error (429 Too Many Requests)

```json
{
  "code": 429,
  "id": "request-123",
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "message": "MAX_QUEUE_LENGTH (10) reached",
  "pid": 12345,
  "queue_id": 1234567890,
  "queue_length": 10,
  "build_number": "1.0.0"
}
```

### Ejemplo de error (500 Internal Server Error)

```json
{
  "code": 500,
  "id": "request-123",
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "message": "Error message describing the exception",
  "pid": 12345,
  "queue_id": 1234567890,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

---

## 5. Manejo de errores

* Parámetros faltantes/incorrectos → 400
* Cola llena → 429
* Excepciones en el proceso → 500

---

## 6. Notas de uso

* `image_url` debe ser válido y accesible.
* `length`: entre 1 y 60 segundos.
* `frame_rate`: entre 15 y 60 fps.
* `zoom_speed`: entre 0 y 100.
* `webhook_url` es opcional pero recomendable.
* `id` facilita seguimiento en logs/notificaciones.

---

## 7. Problemas comunes

* URL inválida o inaccesible.
* Valores fuera de rango → 400.
* Cola llena sin bypass → 429.

---

## 8. Buenas prácticas

* Validar `image_url` antes de enviar.
* Usar `webhook_url` para no hacer *polling*.
* Incluir `id` para rastrear peticiones.
* Activar `bypass_queue` en casos urgentes.