# Endpoint: Corte de Medios

## 1. Descripción general

El endpoint `/v1/media/cut` corta segmentos específicos de un archivo de audio o video, con posibilidad de aplicar configuraciones de codificación.
Forma parte del *blueprint* `v1` de la API Flask.

---

## 2. Endpoint

* **Ruta:** `/v1/media/cut`
* **Método:** `POST`

---

## 3. Petición

### Cabeceras

* `x-api-key` (obligatorio): clave de autenticación.

### Parámetros en el cuerpo

* `media_url` (string, obligatorio): URL del archivo a cortar.
* `cuts` (array de objetos, obligatorio): segmentos a extraer.

  * `start` (string, obligatorio): inicio en formato `hh:mm:ss.ms`.
  * `end` (string, obligatorio): fin en formato `hh:mm:ss.ms`.
* `video_codec` (string, opcional): códec de video. Por defecto `libx264`.
* `video_preset` (string, opcional): preset de video. Por defecto `medium`.
* `video_crf` (number, opcional): CRF (0–51). Por defecto 23.
* `audio_codec` (string, opcional): códec de audio. Por defecto `aac`.
* `audio_bitrate` (string, opcional): bitrate de audio. Por defecto `128k`.
* `webhook_url` (string, opcional): URL para notificación al finalizar.
* `id` (string, opcional): identificador único.

### Ejemplo de petición

```json
{
  "media_url": "https://example.com/video.mp4",
  "cuts": [
    { "start": "00:00:10.000", "end": "00:00:20.000" },
    { "start": "00:00:30.000", "end": "00:00:40.000" }
  ],
  "video_codec": "libx264",
  "video_preset": "medium",
  "video_crf": 23,
  "audio_codec": "aac",
  "audio_bitrate": "128k",
  "webhook_url": "https://example.com/webhook",
  "id": "peticion-123"
}
```

Ejemplo con cURL:

```bash
curl -X POST \
  https://api.example.com/v1/media/cut \
  -H 'x-api-key: TU_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "media_url": "https://example.com/video.mp4",
    "cuts": [
      { "start": "00:00:10.000", "end": "00:00:20.000" },
      { "start": "00:00:30.000", "end": "00:00:40.000" }
    ],
    "video_codec": "libx264",
    "video_preset": "medium",
    "video_crf": 23,
    "audio_codec": "aac",
    "audio_bitrate": "128k",
    "webhook_url": "https://example.com/webhook",
    "id": "peticion-123"
  }'
```

---

## 4. Respuesta

### Ejemplo de éxito

```json
{
  "code": 200,
  "id": "peticion-123",
  "job_id": "uuid-job",
  "response": {
    "file_url": "https://example.com/output.mp4"
  },
  "message": "success",
  "run_time": 5.234,
  "queue_time": 0.012,
  "total_time": 5.246,
  "pid": 12345,
  "queue_id": 1234567890,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Ejemplo de error

```json
{ "code": 400, "message": "Invalid request payload" }
```

```json
{ "code": 401, "message": "Unauthorized" }
```

```json
{ "code": 500, "message": "Internal Server Error" }
```

---

## 5. Manejo de errores

* Parámetros faltantes o inválidos → 400
* API key ausente/incorrecta → 401
* Error interno inesperado → 500
* Cola llena → 429

---

## 6. Notas de uso

* `media_url` debe ser accesible.
* `cuts` requiere segmentos válidos en formato `hh:mm:ss.ms`.
* Parámetros opcionales permiten configurar codificación.
* `webhook_url` útil para notificación automática.
* `id` facilita rastreo.

---

## 7. Problemas comunes

* URL inválida o inaccesible.
* Parámetros de codificación fuera de rango.
* Segmentos inválidos u overlap en `cuts`.

---

## 8. Buenas prácticas

* Validar parámetros antes de enviar.
* Usar `webhook_url` para asincronía.
* Monitorizar `queue_length` en respuestas.
* Incluir `id` único para correlación y depuración.
