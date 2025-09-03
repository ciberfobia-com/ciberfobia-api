# Endpoint: FFmpeg Compose

## 1. Descripción general

El endpoint `/v1/ffmpeg/compose` permite componer comandos complejos de **FFmpeg** mediante la definición de archivos de entrada, filtros y opciones de salida.  
Forma parte de la API v1 definida en `app.py`. Está diseñado para tareas de procesamiento de medios como manipulación de video/audio, transcodificación y más.

---

## 2. Endpoint

- **Ruta:** `/v1/ffmpeg/compose`  
- **Método:** `POST`

---

## 3. Petición

### Cabeceras

- `x-api-key` (obligatorio): clave de autenticación.

### Parámetros en el cuerpo

- `inputs` (array, obligatorio): lista de archivos de entrada.  
  - `file_url` (string, obligatorio): URL del archivo de entrada.  
  - `options` (array, opcional): opciones FFmpeg para este archivo.  
- `filters` (array, opcional): filtros FFmpeg a aplicar.  
- `outputs` (array, obligatorio): lista de configuraciones de salida.  
- `global_options` (array, opcional): opciones FFmpeg globales.  
- `metadata` (objeto, opcional): metadatos a incluir en la respuesta (`thumbnail`, `filesize`, `duration`, `bitrate`, `encoder`).  
- `webhook_url` (string, obligatorio): URL donde se enviará la respuesta.  
- `id` (string, obligatorio): identificador único de la petición.  

### Ejemplo de petición

```json
{
  "inputs": [
    {
      "file_url": "https://example.com/video1.mp4",
      "options": [
        { "option": "-ss", "argument": 10 },
        { "option": "-t", "argument": 20 }
      ]
    },
    {
      "file_url": "https://example.com/video2.mp4"
    }
  ],
  "filters": [
    { "filter": "hflip" }
  ],
  "outputs": [
    {
      "options": [
        { "option": "-c:v", "argument": "libx264" },
        { "option": "-crf", "argument": 23 }
      ]
    }
  ],
  "global_options": [
    { "option": "-y" }
  ],
  "metadata": {
    "thumbnail": true,
    "filesize": true,
    "duration": true,
    "bitrate": true,
    "encoder": true
  },
  "webhook_url": "https://example.com/webhook",
  "id": "peticion-123"
}
````

**Ejemplo con cURL:**

```bash
curl -X POST \
  https://api.example.com/v1/ffmpeg/compose \
  -H 'x-api-key: TU_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "inputs": [
      { "file_url": "https://example.com/video1.mp4", "options": [ { "option": "-ss", "argument": 10 }, { "option": "-t", "argument": 20 } ] },
      { "file_url": "https://example.com/video2.mp4" }
    ],
    "filters": [ { "filter": "hflip" } ],
    "outputs": [ { "options": [ { "option": "-c:v", "argument": "libx264" }, { "option": "-crf", "argument": 23 } ] } ],
    "global_options": [ { "option": "-y" } ],
    "metadata": { "thumbnail": true, "filesize": true, "duration": true, "bitrate": true, "encoder": true },
    "webhook_url": "https://example.com/webhook",
    "id": "peticion-123"
  }'
```

---

## 4. Respuesta

### Ejemplo de éxito (enviado al `webhook_url`)

```json
{
  "endpoint": "/v1/ffmpeg/compose",
  "code": 200,
  "id": "peticion-123",
  "job_id": "job-id",
  "response": [
    {
      "file_url": "https://storage.example.com/output.mp4",
      "thumbnail_url": "https://storage.example.com/thumb.jpg",
      "filesize": 123456,
      "duration": 45.6,
      "bitrate": 1200,
      "encoder": "libx264"
    }
  ],
  "message": "success",
  "pid": 12345,
  "queue_id": 67890,
  "run_time": 4.32,
  "queue_time": 0.5,
  "total_time": 4.82,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Ejemplo de error

```json
{
  "code": 400,
  "id": "peticion-123",
  "job_id": "job-id",
  "message": "Invalid request payload: 'inputs' is a required property",
  "pid": 123,
  "queue_id": 456,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

---

## 5. Manejo de errores

* **400** → parámetros faltantes o inválidos.
* **401** → API key inválida o ausente.
* **429** → cola llena.
* **500** → error interno inesperado.

---

## 6. Notas de uso

* `inputs` debe contener al menos un archivo.
* `outputs` debe tener al menos una configuración.
* `filters` y `global_options` son opcionales.
* `metadata` permite solicitar datos adicionales sobre el archivo resultante.
* `webhook_url` e `id` son obligatorios.

---

## 7. Problemas comunes

* URLs inválidas o inaccesibles.
* Opciones/filtros de FFmpeg no soportados.
* Cola saturada (429).
* Fallos de red que impidan entregar el webhook.

---

## 8. Buenas prácticas

* Validar las URLs antes de enviar la petición.
* Probar comandos FFmpeg localmente primero.
* Monitorizar la longitud de la cola.
* Implementar reintentos para webhooks fallidos.
* Usar `id` únicos para depuración y seguimiento.