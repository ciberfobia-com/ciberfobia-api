# Endpoint: Conversión de Medios

## 1. Descripción general

El endpoint `/v1/media/convert` convierte archivos de audio o video de un formato a otro.
Forma parte del *blueprint* `v1` que agrupa funcionalidades de medios dentro de la API Flask.

---

## 2. Endpoint

* **Ruta:** `/v1/media/convert`
* **Método:** `POST`

---

## 3. Petición

### Cabeceras

* `x-api-key` (obligatorio): clave de autenticación.

### Parámetros en el cuerpo

* `media_url` (string, obligatorio): URL del archivo a convertir.
* `format` (string, obligatorio): formato de salida deseado.
* `video_codec` (string, opcional): códec de video, por defecto `libx264`.
* `video_preset` (string, opcional): preset de video, por defecto `medium`.
* `video_crf` (number, opcional): CRF de compresión (0–51), por defecto 23.
* `audio_codec` (string, opcional): códec de audio, por defecto `aac`.
* `audio_bitrate` (string, opcional): bitrate de audio, por defecto `128k`.
* `webhook_url` (string, opcional): URL para recibir notificación al finalizar.
* `id` (string, opcional): identificador de la petición.

### Ejemplo de petición

```json
{
  "media_url": "https://example.com/video.mp4",
  "format": "avi",
  "video_codec": "libx264",
  "video_preset": "medium",
  "video_crf": 23,
  "audio_codec": "aac",
  "audio_bitrate": "128k",
  "webhook_url": "https://example.com/webhook",
  "id": "peticion-123"
}
```

---

## 4. Respuesta

### Ejemplo de éxito

```json
{
  "code": 200,
  "id": "peticion-123",
  "job_id": "uuid-job",
  "response": "https://cloud.example.com/converted-video.avi",
  "message": "success",
  "pid": 12345,
  "queue_id": 987654321,
  "run_time": 10.234,
  "queue_time": 0.123,
  "total_time": 10.357,
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
  "message": "Invalid request payload",
  "pid": 12345,
  "queue_id": 987654321,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

---

## 5. Manejo de errores

* **400 Bad Request** → payload faltante o inválido.
* **401 Unauthorized** → API key ausente o inválida.
* **500 Internal Server Error** → error inesperado durante la conversión.

---

## 6. Notas de uso

* `media_url` debe apuntar a un archivo accesible.
* `format` debe ser un formato soportado.
* Parámetros opcionales permiten personalizar la conversión.
* Con `webhook_url` se recibe notificación al finalizar.
* `id` facilita el seguimiento de la petición.

---

## 7. Problemas comunes

* `media_url` inválida o inaccesible.
* `format` no soportado.
* Parámetros fuera de rango (ej. `video_crf > 51`).

---

## 8. Buenas prácticas

* Validar parámetros antes de enviar.
* Usar `id` para rastrear peticiones.
* Añadir `webhook_url` para no depender de *polling*.
* Monitorizar logs para detectar errores.
* Implementar límites o colas si se esperan altos volúmenes.